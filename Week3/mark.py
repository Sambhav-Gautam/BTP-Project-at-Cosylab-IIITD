import json

# Load the filtered recipes from the JSON file
with open("filtered_recipes.json", "r") as json_file:
    recipes = json.load(json_file)

# Count the number of entries
num_entries = len(recipes)
print(f"The JSON file contains {num_entries} entries.")
