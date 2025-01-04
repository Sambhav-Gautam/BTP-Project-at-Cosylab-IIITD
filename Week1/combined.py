import pandas as pd
import ast

# Load the output.csv and stats.csv files
output_df = pd.read_csv('output.csv')
stats_df = pd.read_csv('stats.csv')

# List to store the combined results
results = []

# Iterate over the rows of output.csv
for index, row in output_df.iterrows():
    try:
        recipe_id = row['recipe_id']
        # Convert the string representation of the ingredients list into an actual list
        ingredients = ast.literal_eval(row['ingredients'])
        len_ingredients = len(ingredients)  # Calculate the length of the ingredients list

        # Find the corresponding row in stats.csv for this recipe_id
        stats_row = stats_df[stats_df['Recipe ID'] == recipe_id]

        if not stats_row.empty:
            # Get the value of Ingredients Found in Instructions
            ingredients_found = stats_row['Ingredients Found in Instructions'].values[0]
        else:
            # If no match is found, assume 0
            ingredients_found = 0

        # Add the data to the results list
        results.append((recipe_id, ingredients_found, len_ingredients))

    except Exception as e:
        print(f"Error processing recipe_id {row['recipe_id']}: {e}")

# Convert the results list into a DataFrame
results_df = pd.DataFrame(results, columns=["Recipe ID", "Ingredients Found in Instructions", "len(ingredients)"])

# Save the combined results to a new CSV file
results_df.to_csv('combined_stats.csv', index=False)

# Print the combined results
print("\nCombined Results:")
print(results_df)
