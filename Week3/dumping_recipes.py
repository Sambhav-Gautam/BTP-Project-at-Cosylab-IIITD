import pandas as pd
from urllib.parse import quote_plus
import json
from pymongo import MongoClient

# MongoDB connection details
username = "sambhav22435"
password = quote_plus("Sambhav@Possible@2003")  # Escapes special characters
mongo_url = f"mongodb+srv://{username}:{password}@ttc.qg2bq.mongodb.net/"
database_name = "Turing"  # Use the correct casing
collection_name = "ttc"

# Load the data from the CSV file
file_name = "ingredients_stats.csv"
df = pd.read_csv(file_name)
print(f"Loaded {len(df)} rows from the CSV file.")

# Calculate the percentage of random ingredients found in "instructions"
df['Percentage_in_instructions'] = (df['in_instructions'] / df['total_ingredients']) * 100
print("Calculated percentage of ingredients found in instructions.")

# Filter the rows where the percentage of ingredients in instructions is <= 15%
filtered_df = df[df['Percentage_in_instructions'] <= 15]
print(f"Filtered recipes with <= 15% ingredients in instructions: {len(filtered_df)} recipes.")

# MongoDB client connection
client = MongoClient(mongo_url)
db = client[database_name]
collection = db[collection_name]
print("Connected to MongoDB.")

# Prepare the list of recipes to save
recipes_to_save = []
# For each filtered recipe, query the MongoDB collection to get additional details
for _, row in filtered_df.iterrows():
    sno = row['Sno']
    print(f"Processing recipe with Sno: {sno}")
    
    # Query the MongoDB collection to get the recipe details using 'Sno'
    recipe_data = collection.find_one({"Sno": sno})
    
    if recipe_data:
        # Collect the actual data from MongoDB
        recipe = {
            "Sno": row["Sno"],
            "Random Ingredients": recipe_data.get("Random Ingredients", ""),
            "title": recipe_data.get("title", ""),
            "ingredients": recipe_data.get("ingredients", ""),
            "instructions": recipe_data.get("instructions", "")
        }
        recipes_to_save.append(recipe)
        print(f"Added recipe with Sno {sno} to the list.")
    else:
        print(f"Recipe with Sno '{sno}' not found in the database.")

# Save the filtered recipes as a JSON file
with open("filtered_recipes.json", "w") as json_file:
    json.dump(recipes_to_save, json_file, indent=4)
print(f"Saved {len(recipes_to_save)} recipes to filtered_recipes.json.")

# Optional: Insert into MongoDB (if required)
# collection.insert_many(recipes_to_save)
