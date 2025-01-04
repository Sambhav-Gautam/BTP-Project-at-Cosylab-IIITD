import pandas as pd

# Read the input CSV file
df = pd.read_csv("extracted_ingredients.csv")

# Group the ingredients by Recipe ID and convert them to a list
grouped = df.groupby('Recipe ID')['Ingredient'].apply(list).reset_index()

# Rename columns to match the desired format
grouped.columns = ['recipe_id', 'ingredients']

# Save the resulting dataframe to a new CSV
grouped.to_csv('output.csv', index=False)
