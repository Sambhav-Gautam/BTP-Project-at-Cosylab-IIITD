import pandas as pd
from pymongo import MongoClient
from urllib.parse import quote_plus

# M# MongoDB connection details
username = "sambhav22435"
password = quote_plus("Sambhav@Possible@2003")  # Escapes special characters
mongo_url = f"mongodb+srv://{username}:{password}@ttc.qg2bq.mongodb.net/"
database_name = "Turing"  # Use the correct casing
collection_name = "ttc"

# List of CSV files to be uploaded
csv_files = [
    "10000RecipesWithRandomIngredients1.csv",
    "10000RecipesWithRandomIngredients10.csv",
    "10000RecipesWithRandomIngredients11.csv",
    "10000RecipesWithRandomIngredients12.csv",
    "10000RecipesWithRandomIngredients2.csv",
    "10000RecipesWithRandomIngredients3.csv",
    "10000RecipesWithRandomIngredients4.csv",
    "10000RecipesWithRandomIngredients5.csv",
    "10000RecipesWithRandomIngredients6.csv",
    "10000RecipesWithRandomIngredients7.csv",
    "10000RecipesWithRandomIngredients8.csv",
    "10000RecipesWithRandomIngredients9.csv"
]


# Establish MongoDB connection
client = MongoClient(mongo_url)
db = client[database_name]
collection = db[collection_name]

# Function to upload data from each CSV file
def upload_data_from_csv(csv_file):
    try:
        # Load the CSV data
        data = pd.read_csv(csv_file)

        # Drop the '_id' column if it exists in the dataset
        if '_id' in data.columns:
            data = data.drop('_id', axis=1)

        # Convert DataFrame to a list of dictionaries
        data_dict = data.to_dict("records")

        # Insert data into MongoDB
        collection.insert_many(data_dict)
        print(f"Successfully uploaded {len(data_dict)} records from '{csv_file}'.")

    except Exception as e:
        print(f"An error occurred while processing '{csv_file}':", e)

# Upload data from all CSV files
i = 0
for csv_file in csv_files:
    print(f"i : {i}")
    upload_data_from_csv(csv_file)
    i += 1

# Close the MongoDB connection
client.close()
