import numpy as np
from pymongo import MongoClient

def compute_f1_for_chef(chef):
    """
    Computes the F1 score for a chef using the confusion matrix arrays.
    Positive class is considered as the 'real' recipes.
    """
    TP = len(chef.get("RR", []))  # Real identified as real
    FN = len(chef.get("RF", []))  # Real identified as fake
    FP = len(chef.get("FR", []))  # Fake identified as real

    # If there are no predicted positives or no actual positives, F1 is 0
    if (TP + FP) == 0 or (TP + FN) == 0:
        return 0

    precision = TP / (TP + FP)
    recall = TP / (TP + FN)

    if (precision + recall) == 0:
        return 0

    return 2 * precision * recall / (precision + recall)

def compute_skew(chef):
    """
    Computes the ratio of 'real' decisions vs. 'fake' decisions.
    A highly skewed decision pattern might indicate a non-serious evaluation.
    """
    real_decisions = len(chef.get("RR", [])) + len(chef.get("FR", []))
    fake_decisions = len(chef.get("RF", [])) + len(chef.get("FF", []))
    total_decisions = real_decisions + fake_decisions

    if total_decisions == 0:
        return 0, 0  # Avoid division by zero; treat as no decisions made

    real_ratio = real_decisions / total_decisions
    fake_ratio = fake_decisions / total_decisions
    return real_ratio, fake_ratio

def filter_chefs_advanced(db_uri, db_name='trying', collection_name='users',
                          min_f1_threshold=0.6, min_total=5, skew_threshold=0.9):
    """
    Connects to MongoDB, retrieves chef data, computes individual F1 scores,
    verifies that the decision distribution is not overly skewed, and applies
    a z-score filter on F1 scores to remove statistical outliers.
    
    Also logs detailed reasons for why a chef was removed.
    Returns:
      - all_chefs: All chef documents.
      - filtered_chefs: Chefs that pass the filtering criteria.
      - global_f1: Global F1 score computed on the filtered chefs.
      - removal_reasons: A dictionary mapping chef display names to a list of removal reasons.
    """
    client = MongoClient(db_uri)
    db = client[db_name]
    collection = db[collection_name]

    chefs = list(collection.find())
    candidate_chefs = []
    removal_reasons = {}  # To store detailed reasons why a chef is removed

    # First pass: compute metrics and apply basic filters for each chef.
    for chef in chefs:
        chef_f1 = compute_f1_for_chef(chef)
        chef["computed_f1"] = chef_f1

        total_evals = (len(chef.get("RR", [])) + len(chef.get("RF", [])) +
                       len(chef.get("FR", [])) + len(chef.get("FF", [])))
        chef["computed_total"] = total_evals

        reasons = []  # Reasons why this chef might be removed

        # Check minimum evaluations
        if total_evals < min_total:
            reasons.append(f"Insufficient evaluations ({total_evals} < {min_total})")

        # Check F1 threshold
        if chef_f1 < min_f1_threshold:
            reasons.append(f"Low F1 score ({chef_f1:.2f} < {min_f1_threshold})")

        # Check for skewed decision distribution
        real_ratio, fake_ratio = compute_skew(chef)
        if real_ratio > skew_threshold or fake_ratio > skew_threshold:
            reasons.append(f"Skewed decision distribution (real_ratio: {real_ratio:.2f}, fake_ratio: {fake_ratio:.2f} > {skew_threshold})")

        # If any reason exists, record it; otherwise, add chef to candidate list
        if reasons:
            removal_reasons[chef.get("displayName", "Unknown")] = reasons
        else:
            candidate_chefs.append(chef)

    # Optional: further filter based on z-score of the F1 scores.
    filtered_chefs = []
    if candidate_chefs:
        f1_scores = np.array([chef["computed_f1"] for chef in candidate_chefs])
        mean_f1 = np.mean(f1_scores)
        std_f1 = np.std(f1_scores)
        threshold = mean_f1 - std_f1
        for chef in candidate_chefs:
            if chef["computed_f1"] >= threshold:
                filtered_chefs.append(chef)
            else:
                # Log reason for removal due to z-score filtering
                name = chef.get("displayName", "Unknown")
                reason = f"Z-score outlier (F1: {chef['computed_f1']:.2f} < threshold: {threshold:.2f})"
                # Append if already exists; otherwise, add new entry
                if name in removal_reasons:
                    removal_reasons[name].append(reason)
                else:
                    removal_reasons[name] = [reason]
    else:
        filtered_chefs = []

    # Recalculate a global F1 score based on the filtered chefs.
    global_TP = sum(len(chef.get("RR", [])) for chef in filtered_chefs)
    global_FN = sum(len(chef.get("RF", [])) for chef in filtered_chefs)
    global_FP = sum(len(chef.get("FR", [])) for chef in filtered_chefs)

    if (global_TP + global_FP) == 0 or (global_TP + global_FN) == 0:
        global_f1 = 0
    else:
        global_precision = global_TP / (global_TP + global_FP)
        global_recall = global_TP / (global_TP + global_FN)
        global_f1 = 2 * global_precision * global_recall / (global_precision + global_recall)

    return chefs, filtered_chefs, global_f1, removal_reasons

def analyze_chef_filtering(db_uri, db_name='trying', collection_name='users',
                           min_f1_threshold=0.6, min_total=5, skew_threshold=0.9):
    """
    Analyzes the filtering process by comparing overall chef data with the filtered results.
    Prints out:
      - Total chefs before filtering.
      - Total chefs after filtering.
      - List of chef names removed along with detailed reasons.
      - Global F1 score before and after filtering.
      - Improvement in global F1 score.
    """
    client = MongoClient(db_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Retrieve all chefs and compute overall global F1 score (before filtering)
    all_chefs = list(collection.find())
    global_TP_all = sum(len(chef.get("RR", [])) for chef in all_chefs)
    global_FN_all = sum(len(chef.get("RF", [])) for chef in all_chefs)
    global_FP_all = sum(len(chef.get("FR", [])) for chef in all_chefs)

    if (global_TP_all + global_FP_all) == 0 or (global_TP_all + global_FN_all) == 0:
        global_f1_before = 0
    else:
        global_precision_all = global_TP_all / (global_TP_all + global_FP_all)
        global_recall_all = global_TP_all / (global_TP_all + global_FN_all)
        global_f1_before = 2 * global_precision_all * global_recall_all / (global_precision_all + global_recall_all)

    # Use the advanced filtering function and get detailed removal reasons.
    all_chefs, serious_chefs, global_f1_after, removal_reasons = filter_chefs_advanced(
        db_uri, db_name, collection_name, min_f1_threshold, min_total, skew_threshold)

    # Prepare chef name lists for comparison
    all_names = [chef.get("displayName", "Unknown") for chef in all_chefs]
    serious_names = [chef.get("displayName", "Unknown") for chef in serious_chefs]
    removed_names = sorted(list(set(all_names) - set(serious_names)))

    # Print summary report
    print("=== Filtering Summary Report ===")
    print("Total Chefs Before Filtering:", len(all_chefs))
    print("Total Chefs After Filtering:", len(serious_chefs))
    print("Chefs Removed:", removed_names)
    print("Global F1 Score Before Filtering:", global_f1_before)
    print("Global F1 Score After Filtering:", global_f1_after)
    improvement = global_f1_after - global_f1_before
    print("Improvement in Global F1 Score:", improvement)
    print("\nDetailed Removal Reasons:")
    for chef_name in removed_names:
        reasons = removal_reasons.get(chef_name, ["Unknown reason"])
        print(f" - {chef_name}: {', '.join(reasons)}")

    # Return the report data for further processing if needed.
    return {
        "total_before": len(all_chefs),
        "total_after": len(serious_chefs),
        "removed_chefs": removed_names,
        "removal_details": removal_reasons,
        "global_f1_before": global_f1_before,
        "global_f1_after": global_f1_after,
        "improvement": improvement
    }

# Example usage:
db_uri = "mongodb+srv://sambhavsingh911:nigganigga@tcluster0.osayr3i.mongodb.net/"
report = analyze_chef_filtering(db_uri)
