import pandas as pd

# Load the combined_stats.csv file
combined_stats_df = pd.read_csv('combined_stats.csv')

# Validate the condition: Ingredients Found in Instructions <= len(ingredients)
valid_rows = combined_stats_df[
    combined_stats_df['Ingredients Found in Instructions'] > combined_stats_df['len(ingredients)']
]

# Count the number of valid rows
valid_count = len(valid_rows)

# Print the result
print(f"Number of rows where 'Ingredients Found in Instructions' > 'len(ingredients)': {valid_count}")
