import json
from urllib.parse import quote_plus
from pymongo import MongoClient

# MongoDB connection details
username = "sambhav22435"
password = quote_plus("Sambhav@Possible@2003")  # Escapes special characters
mongo_url = f"mongodb+srv://{username}:{password}@ttc.qg2bq.mongodb.net/"
database_name = "Turing"  # Use the correct casing
collection_name = "ttc"

# MongoDB client connection
client = MongoClient(mongo_url)
db = client[database_name]
collection = db[collection_name]
print("Connected to MongoDB.")

# Load the recipes from the JSON file
with open("filtered_recipes.json", "r") as json_file:
    recipes = json.load(json_file)

# Extract the 'Sno' values from the recipes
snos_to_delete = [recipe["Sno"] for recipe in recipes]

# Delete the recipes from the 'ttc' collection based on 'Sno'
result = collection.delete_many({"Sno": {"$in": snos_to_delete}})

# Output the number of deleted recipes
print(f"Deleted {result.deleted_count} recipes from the collection.")
