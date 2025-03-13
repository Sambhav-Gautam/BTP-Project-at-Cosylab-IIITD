import pymongo
import csv
from urllib.parse import quote_plus

# M# MongoDB connection details
username = "sambhav22435"
password = quote_plus("Sambhav@Possible@2003")  # Escapes special characters
mongo_url = f"mongodb+srv://{username}:{password}@ttc.qg2bq.mongodb.net/"
database_name = "Turing"  # Use the correct casing
collection_name = "ttc"

# Connect to MongoDB
client = pymongo.MongoClient(mongo_url)
db = client[database_name]
collection = db[collection_name]

# Function to count ingredient presence
def ingredient_stats(recipe):
    random_ingredients = recipe["Random Ingredients"].split(",")
    instructions = recipe["instructions"].lower()
    ingredients = recipe["ingredients"].lower()
    
    total_ingredients = len(random_ingredients)
    in_instructions = 0
    in_ingredients = 0

    for ing in random_ingredients:
        check_one_time = ing.split(" ")
        for i in check_one_time:
            plural = i + "s"
            singular = i[:-1]
            if i.lower() in instructions or plural.lower() in instructions or singular.lower() in instructions:
                in_instructions += 1
                break
        for i in check_one_time:
            plural = i + "s"
            singular = i[:-1]
            if i.lower() in ingredients or plural.lower() in ingredients or singular.lower() in ingredients:
                in_ingredients += 1
                break
        

    return {
        "Sno": recipe["Sno"],
        "title": recipe["title"],
        "total_ingredients": total_ingredients,
        "in_instructions": in_instructions,
        "in_ingredients": in_ingredients
    }

# Analyze and save results
stats = []
total_recipes = collection.count_documents({})
print(f"Total recipes to process: {total_recipes}")

for index, recipe in enumerate(collection.find(), start=1):
    print(f"Processing recipe {index}/{total_recipes}: {recipe['title']}") 
    stats.append(ingredient_stats(recipe))
    
# Define CSV keys
keys = ["Sno", "title", "total_ingredients", "in_instructions", "in_ingredients"]

# Write to CSV with UTF-8 encoding
with open("ingredients_stats_after_deleting.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=keys)
    writer.writeheader()
    writer.writerows(stats)

print("Analysis completed. Results saved to 'ingredients_stats.csv'.")