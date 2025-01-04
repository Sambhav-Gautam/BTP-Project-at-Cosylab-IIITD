import pandas as pd
from pymongo import MongoClient
import ast

# MongoDB connection string
connection_string = "mongodb+srv://sambhavsingh911:nigganigga@tcluster0.osayr3i.mongodb.net/"

# Connect to MongoDB
try:
    # Connect to the MongoDB cluster
    client = MongoClient(connection_string)

    # Access the 'trying' database
    db = client['trying']

    # Access the 'recipegs' collection
    collection = db['recipegs']
    print("Successfully connected to MongoDB!")

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Load the output CSV file containing ingredients
df = pd.read_csv('output.csv')

# List to store results
results = []

# Iterate over the DataFrame to check how many ingredients are present in the instructions
for index, row in df.iterrows():
    try:
        recipe_id = row['recipe_id']
        # Convert the ingredients from string to a list
        print(f"Processing Recipe ID: {recipe_id}")
        ingredients = ast.literal_eval(row['ingredients'])

        # Fetch the recipe document from the MongoDB collection using the recipe_id
        recipe = collection.find_one({"Sno": recipe_id})

        if recipe:
            # Fetch the instructions of the recipe
            instructions = recipe.get("instructions", "").lower()

            # Count how many ingredients are in the instructions
            found_ingredients = [ingredient for ingredient in ingredients if ingredient.lower() in instructions]

            # Store the count of found ingredients for the current recipe
            results.append((recipe_id, len(found_ingredients)))

        else:
            results.append((recipe_id, 0))  # Recipe not found

    except Exception as e:
        print(f"Error processing recipe {row['recipe_id']}: {e}")
        results.append((row['recipe_id'], 0))  # In case of error, assume 0 ingredients found

# Convert the results to a DataFrame
results_df = pd.DataFrame(results, columns=["Recipe ID", "Ingredients Found in Instructions"])

# Save the results to a CSV file
results_df.to_csv('stats.csv', index=False)

# Print the results
print("\nStats Results:")
print(results_df)
