import csv
from pymongo import MongoClient

# MongoDB connection string
connection_string = "mongodb+srv://sambhavsingh911:nigganigga@tcluster0.osayr3i.mongodb.net/"

# Connect to MongoDB
try:
    # Connect to the MongoDB cluster
    client = MongoClient(connection_string)

    # Access the 'trying' database and the 'recipegs' collection
    db = client['trying']
    collection = db['recipegs']
    print("Successfully connected to MongoDB!")

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

# Function to check completeness
def is_complete(recipe):
    required_fields = ['title', 'ingredients', 'instructions']
    for field in required_fields:
        if not recipe.get(field) or recipe[field].strip() == "":
            return False
    return True

# Function to detect duplicate recipes
def is_duplicate(recipe, existing_recipes):
    for existing in existing_recipes:
        if (existing['title'] == recipe['title'] and
                existing['ingredients'] == recipe['ingredients'] and
                existing['instructions'] == recipe['instructions']):
            return True
    return False

# Main filtering function
def filter_recipes(collection):
    filtered_recipes = []
    recipes = list(collection.find())
    total_recipes = len(recipes)

    for i, recipe in enumerate(recipes):
        # Show progress
        print(f"Currently processing recipe {i+1} out of {total_recipes}: {recipe['title']}")

        # Check completeness
        if not is_complete(recipe):
            continue

        # Check for duplicates
        if is_duplicate(recipe, filtered_recipes):
            continue

        # If the recipe passes all checks, add to filtered list
        filtered_recipes.append(recipe)

    return filtered_recipes

# Function to save filtered recipe count and current recipe being evaluated to CSV
def save_count_and_recipe_to_csv(filtered_recipes, current_recipe, filename='filtered_recipes_count.csv'):
    # Open the CSV file for writing
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write headers
        writer.writerow(['Filtered Recipes Count', 'Currently Evaluating Recipe Title', 'Currently Evaluating Recipe Ingredients'])
        
        # Write the count of filtered recipes and the current recipe's details
        writer.writerow([len(filtered_recipes), current_recipe['title'], current_recipe['ingredients']])
    
    print(f"Filtered recipe count and current recipe details saved to {filename}")

# Perform filtering and track the current recipe
filtered_recipes = filter_recipes(collection)

# Save filtered recipe count and current recipe to CSV
# Assuming the current recipe being evaluated is the last one in the list
if filtered_recipes:
    current_recipe = filtered_recipes[-1]
    save_count_and_recipe_to_csv(filtered_recipes, current_recipe)
else:
    print("No recipes passed the filter.")
