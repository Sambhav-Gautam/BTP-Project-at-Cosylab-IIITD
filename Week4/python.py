import pymongo
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Connect to MongoDB using the provided connection string
client = pymongo.MongoClient('mongodb+srv://sambhavsingh911:nigganigga@tcluster0.osayr3i.mongodb.net/')
# Replace 'your_db_name' and 'your_collection_name' with your actual database and collection names
db = client['trying']
collection = db['users']

# Define the time thresholds (in seconds) to filter evaluations based on average time per recipe
thresholds = [10, 20, 30]

# Dictionary to store results for each threshold
results = {}

# Loop over each threshold
for threshold in thresholds:
    # Initialize counters for evaluation categories for this threshold
    total_ff = 0  # Actual Fake predicted as Fake
    total_fr = 0  # Actual Fake predicted as Real
    total_rf = 0  # Actual Real predicted as Fake
    total_rr = 0  # Actual Real predicted as Real

    # Retrieve all documents from the collection
    docs = collection.find({})
    for doc in docs:
        recipes = doc.get("recipe_evaluated", [])
        # If no recipes evaluated, skip this document
        if not recipes:
            continue
        
        # Calculate session time in seconds using createdAt and updatedAt
        created_at = doc.get("createdAt")
        updated_at = doc.get("updatedAt")
        # Skip the document if the timestamps are missing
        if not created_at or not updated_at:
            continue

        session_time = (updated_at - created_at).total_seconds()
        # Compute average time per recipe
        avg_time = session_time / len(recipes)
        
        # Only include this document if the average evaluation time meets the threshold
        if avg_time < threshold:
            continue
        
        # Aggregate counts from the evaluation outcome arrays
        total_ff += len(doc.get("FF", []))
        total_fr += len(doc.get("FR", []))
        total_rf += len(doc.get("RF", []))
        total_rr += len(doc.get("RR", []))
    
    # Build the 2x2 confusion matrix
    # Rows: Actual classes [Fake, Real]
    # Columns: Predicted classes [Fake, Real]
    conf_matrix = np.array([[total_ff, total_fr],
                            [total_rf, total_rr]])

    # Compute evaluation metrics for the Fake class (treated as positive)
    precision_fake = total_ff / (total_ff + total_rf) if (total_ff + total_rf) > 0 else 0
    recall_fake    = total_ff / (total_ff + total_fr) if (total_ff + total_fr) > 0 else 0
    f1_fake        = (2 * precision_fake * recall_fake / (precision_fake + recall_fake)
                      if (precision_fake + recall_fake) > 0 else 0)

    # Compute evaluation metrics for the Real class (treating Real as positive)
    precision_real = total_rr / (total_rr + total_fr) if (total_rr + total_fr) > 0 else 0
    recall_real    = total_rr / (total_rr + total_rf) if (total_rr + total_rf) > 0 else 0
    f1_real        = (2 * precision_real * recall_real / (precision_real + recall_real)
                      if (precision_real + recall_real) > 0 else 0)

    # Compute the macro F1 score (average of the two classes)
    macro_f1 = (f1_fake + f1_real) / 2

    # Store results for this threshold
    results[threshold] = {
        "conf_matrix": conf_matrix,
        "precision_fake": precision_fake,
        "recall_fake": recall_fake,
        "f1_fake": f1_fake,
        "precision_real": precision_real,
        "recall_real": recall_real,
        "f1_real": f1_real,
        "macro_f1": macro_f1
    }

    # Print out stats for this threshold
    print(f"\nThreshold: {threshold} seconds (Average Time per Recipe)")
    print("Confusion Matrix:")
    print(conf_matrix)
    print(f"Fake Class - Precision: {precision_fake:.2f}, Recall: {recall_fake:.2f}, F1 Score: {f1_fake:.2f}")
    print(f"Real Class - Precision: {precision_real:.2f}, Recall: {recall_real:.2f}, F1 Score: {f1_real:.2f}")
    print(f"Macro F1 Score: {macro_f1:.2f}")

# Plot confusion matrices for all thresholds side by side
fig, axes = plt.subplots(1, len(thresholds), figsize=(5 * len(thresholds), 4))
if len(thresholds) == 1:
    axes = [axes]

for ax, threshold in zip(axes, thresholds):
    cm = results[threshold]["conf_matrix"]
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Predicted Fake', 'Predicted Real'],
                yticklabels=['Actual Fake', 'Actual Real'],
                ax=ax)
    ax.set_title(f"Threshold: {threshold} sec")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
plt.tight_layout()
plt.show()
