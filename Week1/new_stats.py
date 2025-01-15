import csv
import random

# File names
input_file_name = 'combined_stats.csv'
output_file_name = 'newdataset.csv'

# Read the data from the CSV file
def read_csv(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Get the header row
        data = [row for row in reader]
    return header, data

# Write the modified data to a new CSV file
def write_csv(file_name, header, data):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

# Modify the data to satisfy the condition
def modify_data(data):
    f = False
    for row in data:
        ingredients_found = int(row[1])
        len_ingredients = int(row[2])
        if f:
            f = False
        else:
            f = True
        # Ensure len(ingredients) >= Ingredients Found in Instructions
        if ingredients_found < len_ingredients and f:
            increase_by = 1
            while (ingredients_found + increase_by) < len_ingredients:
                increase_by += 1
                break
            row[1] = str(ingredients_found + increase_by)
    return data

# Main program
if __name__ == "__main__":
    header, data = read_csv(input_file_name)
    modified_data = modify_data(data)
    write_csv(output_file_name, header, modified_data)
    print(f"Created {output_file_name} successfully.")