import json
from urllib.parse import quote_plus
from pymongo import MongoClient

# MongoDB connection details
username = "sambhav22435"
password = quote_plus("Sambhav@Possible@2003")  # Escapes special characters
mongo_url = f"mongodb+srv://{username}:{password}@ttc.qg2bq.mongodb.net/"
database_name = "Turing"  # Use the correct casing
collection_name = "Dumped"

# MongoDB client connection
client = MongoClient(mongo_url)
db = client[database_name]
collection = db[collection_name]
print("Connected to MongoDB.")

# Load the recipes from the JSON file
with open("filtered_recipes.json", "r") as json_file:
    recipes = json.load(json_file)

# Insert the recipes into the 'Dumped' collection
result = collection.insert_many(recipes)
print(f"Inserted {len(result.inserted_ids)} recipes into the collection.")
