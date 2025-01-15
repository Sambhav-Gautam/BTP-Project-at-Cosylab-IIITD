import pandas as pd

# Load the data from the CSV file
file_name = "ingredients_stats.csv"
df = pd.read_csv(file_name)

# Calculate the percentage of random ingredients found in "ingredients"
df['Percentage_in_ingredients'] = (df['in_ingredients'] / df['total_ingredients']) * 100

# Filter recipes where Percentage_in_ingredients == 0
recipes_with_zero_percentage = df[df['Percentage_in_ingredients'] == 0]

# Extract the "Sno" (recipe IDs)
recipe_ids_with_zero_percentage = recipes_with_zero_percentage[['Sno']]

# Save the result to a new CSV file
output_file = "recipes_with_zero_percentage.csv"
recipe_ids_with_zero_percentage.to_csv(output_file, index=False)

# Print the path of the output CSV file
print(f"Recipe IDs with zero percentage saved to: {output_file}")