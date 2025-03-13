import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# -----------------------------
# Summary Data for Each Threshold
# -----------------------------
data_summary = {
    'min_f1_threshold': [0.10, 0.20, 0.30, 0.40, 0.50, 0.60],
    'total_chefs_before': [29, 29, 29, 29, 29, 29],
    'total_chefs_after': [20, 12, 6, 4, 4, 3],
    'global_f1_before': [0.4819, 0.4819, 0.4819, 0.4819, 0.4819, 0.4819],
    'global_f1_after': [0.4980, 0.5217, 0.5578, 0.6260, 0.6260, 0.6640],
    'total_recipes': [2165, 1952, 1566, 715, 715, 236]
}
df_summary = pd.DataFrame(data_summary)
df_summary['chefs_removed'] = df_summary['total_chefs_before'] - df_summary['total_chefs_after']

# -----------------------------
# Detailed Removal Reasons Data
# (Only the key reasons are considered.)
# -----------------------------
removal_data = [
    # Threshold 0.10
    {'min_f1_threshold': 0.10, 'Chef': 'Ansh Mittal', 'Reason': 'Insufficient evaluations (0 < 5), Low F1 score (0.00 < 0.1)'},
    {'min_f1_threshold': 0.10, 'Chef': 'Rizwan Yargatti', 'Reason': 'Insufficient evaluations (1 < 5), Low F1 score (0.00 < 0.1), Skewed decision distribution (real_ratio: 0.00, fake_ratio: 1.00 > 0.9)'},
    {'min_f1_threshold': 0.10, 'Chef': 'Mahek Panjabi', 'Reason': 'Low F1 score (0.00 < 0.1)'},
    {'min_f1_threshold': 0.10, 'Chef': 'Priyanshi Agrawal', 'Reason': 'Low F1 score (0.10 < 0.1)'},
    {'min_f1_threshold': 0.10, 'Chef': 'Siddharth Bose', 'Reason': 'Insufficient evaluations (0 < 5), Low F1 score (0.00 < 0.1)'},
    {'min_f1_threshold': 0.10, 'Chef': 'Aayushri Srivastava', 'Reason': 'Low F1 score (0.00 < 0.1)'},
    {'min_f1_threshold': 0.10, 'Chef': 'Soniya Premchandani', 'Reason': 'Insufficient evaluations (0 < 5), Low F1 score (0.00 < 0.1)'},
    {'min_f1_threshold': 0.10, 'Chef': 'Fathima Sainudheen', 'Reason': 'Z-score outlier (F1: 0.10 < threshold: 0.13)'},
    {'min_f1_threshold': 0.10, 'Chef': 'Jasleen Kaur', 'Reason': 'Z-score outlier (F1: 0.13 < threshold: 0.13)'},
    # Threshold 0.20
    {'min_f1_threshold': 0.20, 'Chef': 'Ansh Mittal', 'Reason': 'Insufficient evaluations (0 < 5), Low F1 score (0.00 < 0.2)'},
    {'min_f1_threshold': 0.20, 'Chef': 'Rizwan Yargatti', 'Reason': 'Insufficient evaluations (1 < 5), Low F1 score (0.00 < 0.2), Skewed decision distribution (real_ratio: 0.00, fake_ratio: 1.00 > 0.9)'},
    {'min_f1_threshold': 0.20, 'Chef': 'Tanay Jounjat', 'Reason': 'Low F1 score (0.19 < 0.2)'},
    {'min_f1_threshold': 0.20, 'Chef': 'Mahek Panjabi', 'Reason': 'Low F1 score (0.00 < 0.2)'},
    {'min_f1_threshold': 0.20, 'Chef': 'Fathima Sainudheen', 'Reason': 'Low F1 score (0.10 < 0.2)'},
    {'min_f1_threshold': 0.20, 'Chef': 'loboangel moses', 'Reason': 'Low F1 score (0.15 < 0.2)'},
    {'min_f1_threshold': 0.20, 'Chef': 'Meet Shah', 'Reason': 'Low F1 score (0.17 < 0.2)'},
    {'min_f1_threshold': 0.20, 'Chef': 'Rishita Godre', 'Reason': 'Low F1 score (0.16 < 0.2)'},
    {'min_f1_threshold': 0.20, 'Chef': 'Prem Gujar', 'Reason': 'Low F1 score (0.14 < 0.2)'},
    {'min_f1_threshold': 0.20, 'Chef': 'Kruti Anegundi', 'Reason': 'Low F1 score (0.15 < 0.2)'},
    {'min_f1_threshold': 0.20, 'Chef': 'Priyanshi Agrawal', 'Reason': 'Low F1 score (0.10 < 0.2)'},
    {'min_f1_threshold': 0.20, 'Chef': 'Jasleen Kaur', 'Reason': 'Low F1 score (0.13 < 0.2)'},
    {'min_f1_threshold': 0.20, 'Chef': 'Siddharth Bose', 'Reason': 'Insufficient evaluations (0 < 5), Low F1 score (0.00 < 0.2)'},
    {'min_f1_threshold': 0.20, 'Chef': 'Aayushri Srivastava', 'Reason': 'Low F1 score (0.00 < 0.2)'},
    {'min_f1_threshold': 0.20, 'Chef': 'Soniya Premchandani', 'Reason': 'Insufficient evaluations (0 < 5), Low F1 score (0.00 < 0.2)'},
    {'min_f1_threshold': 0.20, 'Chef': 'Bhumii Sharma', 'Reason': 'Z-score outlier (F1: 0.20 < threshold: 0.25)'},
    {'min_f1_threshold': 0.20, 'Chef': 'Sanjana Sapkal', 'Reason': 'Z-score outlier (F1: 0.20 < threshold: 0.25)'},
    # Threshold 0.30
    {'min_f1_threshold': 0.30, 'Chef': 'Ansh Mittal', 'Reason': 'Insufficient evaluations (0 < 5), Low F1 score (0.00 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Rizwan Yargatti', 'Reason': 'Insufficient evaluations (1 < 5), Low F1 score (0.00 < 0.3), Skewed decision distribution (real_ratio: 0.00, fake_ratio: 1.00 > 0.9)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Tanay Jounjat', 'Reason': 'Low F1 score (0.19 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Mahek Panjabi', 'Reason': 'Low F1 score (0.00 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Fathima Sainudheen', 'Reason': 'Low F1 score (0.10 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'loboangel moses', 'Reason': 'Low F1 score (0.15 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Bhumii Sharma', 'Reason': 'Low F1 score (0.20 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Meet Shah', 'Reason': 'Low F1 score (0.17 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Krishi Chawla', 'Reason': 'Low F1 score (0.26 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Rishita Godre', 'Reason': 'Low F1 score (0.16 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Prem Gujar', 'Reason': 'Low F1 score (0.14 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Kruti Anegundi', 'Reason': 'Low F1 score (0.15 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Priyanshi Agrawal', 'Reason': 'Low F1 score (0.10 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Videesha Sawane', 'Reason': 'Low F1 score (0.27 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Jasleen Kaur', 'Reason': 'Low F1 score (0.13 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Sanjana Sapkal', 'Reason': 'Low F1 score (0.20 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Siddharth Bose', 'Reason': 'Insufficient evaluations (0 < 5), Low F1 score (0.00 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'yashi yashi', 'Reason': 'Low F1 score (0.27 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Aayushri Srivastava', 'Reason': 'Low F1 score (0.00 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Soniya Premchandani', 'Reason': 'Insufficient evaluations (0 < 5), Low F1 score (0.00 < 0.3)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Sakshi Dahiphale', 'Reason': 'Z-score outlier (F1: 0.34 < threshold: 0.39)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Japtej Singh', 'Reason': 'Z-score outlier (F1: 0.36 < threshold: 0.39)'},
    {'min_f1_threshold': 0.30, 'Chef': 'Devyani. Dangat', 'Reason': 'Z-score outlier (F1: 0.38 < threshold: 0.39)'},
    # Threshold 0.40 (and similar for 0.50; here we include a few sample entries)
    {'min_f1_threshold': 0.40, 'Chef': 'Ansh Mittal', 'Reason': 'Insufficient evaluations (0 < 5), Low F1 score (0.00 < 0.4)'},
    {'min_f1_threshold': 0.40, 'Chef': 'Rizwan Yargatti', 'Reason': 'Insufficient evaluations (1 < 5), Low F1 score (0.00 < 0.4), Skewed decision distribution (real_ratio: 0.00, fake_ratio: 1.00 > 0.9)'},
    {'min_f1_threshold': 0.40, 'Chef': 'Tanay Jounjat', 'Reason': 'Low F1 score (0.19 < 0.4)'},
    {'min_f1_threshold': 0.40, 'Chef': 'Mahek Panjabi', 'Reason': 'Low F1 score (0.00 < 0.4)'},
    {'min_f1_threshold': 0.40, 'Chef': 'Fathima Sainudheen', 'Reason': 'Low F1 score (0.10 < 0.4)'},
    {'min_f1_threshold': 0.40, 'Chef': 'loboangel moses', 'Reason': 'Low F1 score (0.15 < 0.4)'},
    {'min_f1_threshold': 0.40, 'Chef': 'Bhumii Sharma', 'Reason': 'Low F1 score (0.20 < 0.4)'},
    {'min_f1_threshold': 0.40, 'Chef': 'Meet Shah', 'Reason': 'Low F1 score (0.17 < 0.4)'},
    {'min_f1_threshold': 0.40, 'Chef': 'Krishi Chawla', 'Reason': 'Low F1 score (0.26 < 0.4)'},
    {'min_f1_threshold': 0.40, 'Chef': 'Rishita Godre', 'Reason': 'Low F1 score (0.16 < 0.4)'},
    # Threshold 0.60 (sample entries)
    {'min_f1_threshold': 0.60, 'Chef': 'Ansh Mittal', 'Reason': 'Insufficient evaluations (0 < 5), Low F1 score (0.00 < 0.6)'},
    {'min_f1_threshold': 0.60, 'Chef': 'Rizwan Yargatti', 'Reason': 'Insufficient evaluations (1 < 5), Low F1 score (0.00 < 0.6), Skewed decision distribution (real_ratio: 0.00, fake_ratio: 1.00 > 0.9)'},
    {'min_f1_threshold': 0.60, 'Chef': 'Tanay Jounjat', 'Reason': 'Low F1 score (0.19 < 0.6)'},
    {'min_f1_threshold': 0.60, 'Chef': 'Ritu Ganthade', 'Reason': 'Z-score outlier (F1: 0.61 < threshold: 0.62)'}
]
df_removals = pd.DataFrame(removal_data)

# -----------------------------
# Process Removal Reasons into 4 Categories
# -----------------------------
df_removals['Insufficient'] = df_removals['Reason'].str.contains("Insufficient evaluations", case=False).astype(int)
df_removals['Low_F1']      = df_removals['Reason'].str.contains("Low F1 score", case=False).astype(int)
df_removals['Skewed']      = df_removals['Reason'].str.contains("Skewed decision distribution", case=False).astype(int)
df_removals['Z_score']     = df_removals['Reason'].str.contains("Z-score outlier", case=False).astype(int)

# Aggregate counts for each reason per threshold
reason_counts = df_removals.groupby('min_f1_threshold')[['Insufficient', 'Low_F1', 'Skewed', 'Z_score']].sum().reset_index()

# -----------------------------
# Create the Dashboard (2 Rows)
# -----------------------------
fig, axs = plt.subplots(2, 2, figsize=(16, 12))

# --- Top Left: Global F1 Score (Before vs. After) ---
ax1 = axs[0, 0]
ax1.plot(df_summary['min_f1_threshold'], df_summary['global_f1_before'], marker='o', linestyle='--', label='Before')
ax1.plot(df_summary['min_f1_threshold'], df_summary['global_f1_after'], marker='o', linestyle='-', label='After')
ax1.set_title("Global F1 Score")
ax1.set_xlabel("min_f1_threshold")
ax1.set_ylabel("F1 Score")
ax1.legend()
ax1.grid(True)

# --- Top Right: Chefs Count (Before, After & Removed) ---
ax2 = axs[0, 1]
width = 0.25
x = np.arange(len(df_summary))
ax2.bar(x - width, df_summary['total_chefs_before'], width, label='Before')
ax2.bar(x, df_summary['total_chefs_after'], width, label='After')
ax2.bar(x + width, df_summary['chefs_removed'], width, label='Removed', color='salmon')
ax2.set_title("Chefs Count")
ax2.set_xlabel("min_f1_threshold")
ax2.set_ylabel("Number of Chefs")
ax2.set_xticks(x)
ax2.set_xticklabels(df_summary['min_f1_threshold'])
ax2.legend()
ax2.grid(True)

# --- Bottom Left: Stacked Bar Chart for Removal Reasons ---
ax3 = axs[1, 0]
x_rc = np.arange(len(reason_counts))
p1 = ax3.bar(x_rc, reason_counts['Insufficient'], label='Insufficient Evaluations')
p2 = ax3.bar(x_rc, reason_counts['Low_F1'], bottom=reason_counts['Insufficient'], label='Low F1 Score')
p3 = ax3.bar(x_rc, reason_counts['Skewed'], 
             bottom=reason_counts['Insufficient'] + reason_counts['Low_F1'],
             label='Skewed Distribution')
p4 = ax3.bar(x_rc, reason_counts['Z_score'], 
             bottom=reason_counts['Insufficient'] + reason_counts['Low_F1'] + reason_counts['Skewed'],
             label='Z-score Outlier')
ax3.set_title("Removal Reasons Count by Threshold")
ax3.set_xlabel("min_f1_threshold")
ax3.set_ylabel("Count")
ax3.set_xticks(x_rc)
ax3.set_xticklabels(reason_counts['min_f1_threshold'])
ax3.legend()

# --- Bottom Right: (Optional) Additional Annotation Panel ---
# Here we simply add a text box summarizing the four key removal reasons.
ax4 = axs[1, 1]
ax4.axis('off')
summary_text = (
    "Key Removal Reasons:\n"
    "• Insufficient Evaluations\n"
    "• Low F1 Score\n"
    "• Skewed Decision Distribution\n"
    "• Z-score Outlier"
)
ax4.text(0.5, 0.5, summary_text, ha='center', va='center', fontsize=14, bbox=dict(facecolor='lightblue', alpha=0.5))

plt.tight_layout()
plt.show()
