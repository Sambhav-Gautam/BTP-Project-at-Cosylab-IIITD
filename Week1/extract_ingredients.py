from pymongo import MongoClient
import spacy
import re
import pandas as pd
from collections import defaultdict

# MongoDB connection string
connection_string = "mongodb+srv://sambhavsingh911:nigganigga@tcluster0.osayr3i.mongodb.net/"

# Load SpaCy's NER model
nlp = spacy.load("en_core_web_sm")

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

# Set to store unique ingredients with their recipe ID
unique_ingredients = set()

# Define a function to clean ingredient names
def clean_ingredient_name(name):
    # Remove special characters and digits
    cleaned_name = re.sub(r'[^a-zA-Z\s]', '', name)  # Keep only letters and spaces
    return cleaned_name.strip()

# Fetch all recipes at once using list()
recipes = list(collection.find())
number = 0
# Process each recipe in the list
for recipe in recipes:
    try:
        print(f"{number}")
        
        number += 1
        recipe_id = recipe.get("Sno", None)  # Assuming 'Sno' as the unique recipe identifier
        ingredients = recipe.get("ingredients", "").split('|')  # Assuming ingredients are separated by '|'

        # Process each ingredient phrase
        for ingredient_phrase in ingredients:
            # Apply NER using SpaCy to extract named entities
            doc = nlp(ingredient_phrase)

            # Processing ingredients to extract main ingredient names using POS tagging
            ingredient_parts = []
            for token in doc:
                if token.pos_ in ['NOUN', 'PROPN'] and not token.text.isdigit():
                    ingredient_parts.append(token.text.lower())

            non_keywords = {'cups', 'cup', 'tablespoons', 'tablespoon', 'teaspoons', 'teaspoon', 'optional',
                            'packed', 'all-purpose', 'inch', 'pie', 'shell', 'divided',
                            'smoke', 'chopped', 'roast', 'sliced', 'crushed', 'powder', 'pieces', 'taste', 'packet', 'chuck', ')', ',', '(', 'thinly'}
            filtered_ingredients = [word for word in ingredient_parts if word not in non_keywords]

            # Clean ingredient names and remove any that are empty
            cleaned_ingredients = [clean_ingredient_name(word) for word in filtered_ingredients if clean_ingredient_name(word)]

            if cleaned_ingredients:
                # Add the last cleaned word which often is the ingredient name along with recipe ID
                unique_ingredients.add((recipe_id, cleaned_ingredients[-1]))

    except Exception as e:
        print(f"Error processing recipe {recipe_id}: {e}")
        continue

# Convert the collected data to a DataFrame
df = pd.DataFrame(list(unique_ingredients), columns=["Recipe ID", "Ingredient"])

# Remove duplicates, if needed
df = df.drop_duplicates(subset=["Recipe ID", "Ingredient"])

# Sort the DataFrame by Recipe ID
df = df.sort_values(by="Recipe ID")

# Print the sorted result
print("\nRecipe ID | Ingredient Name")
for index, row in df.iterrows():
    print(f"{row['Recipe ID']} | {row['Ingredient']}")

# Save the results to a CSV file
df.to_csv('extracted_ingredients.csv', index=False)

print("Ingredient extraction complete. Data saved to 'extracted_ingredients.csv'.")
