import pandas as pd

# Load the CSV file
csv_file = 'ingredients_stats.csv'
df = pd.read_csv(csv_file)

# Filter rows where the condition is not met
condition_not_met = (df['total_ingredients'] < df['in_instructions']) | (df['in_ingredients'] > df['total_ingredients'])

# Count the number of recipes that do not meet the criteria
count_not_following = condition_not_met.sum()

# Print the result
print(f"Number of recipes that do not follow the conditions: {count_not_following}")
