import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Load the data from the CSV file
file_name = "ingredients_stats_after_deleting.csv"
df = pd.read_csv(file_name)

# Calculate the percentage of random ingredients found in "instructions" and "ingredients"
df['Percentage_in_instructions'] = (df['in_instructions'] / df['total_ingredients']) * 100
df['Percentage_in_ingredients'] = (df['in_ingredients'] / df['total_ingredients']) * 100

# Create bins and labels for percentage segments (instructions and ingredients)
bins = [-1] + list(range(0, 101, 5))  # Bins from -1 to 100 with steps of 5
labels = ['== 0'] + [f'> {i} and <= {i + 5}' for i in range(0, 95, 5)] + ['> 95 and <= 100']

# Categorize into segments for "in_instructions"
df['Segment_in_instructions'] = pd.cut(
    df['Percentage_in_instructions'],
    bins=bins,
    labels=labels,
    right=True
)

# Categorize into segments for "in_ingredients"
df['Segment_in_ingredients'] = pd.cut(
    df['Percentage_in_ingredients'],
    bins=bins,
    labels=labels,
    right=True
)

# Count occurrences in each segment for the pie chart (instructions)
segment_counts_in_instructions = df['Segment_in_instructions'].value_counts(sort=False)

# Count occurrences in each segment for the pie chart (ingredients)
segment_counts_in_ingredients = df['Segment_in_ingredients'].value_counts(sort=False)

# Create a colormap with distinct colors for each segment
num_segments_in_instructions = len(segment_counts_in_instructions)
cmap_in_instructions = ListedColormap(plt.cm.get_cmap('tab20', num_segments_in_instructions).colors[:num_segments_in_instructions])

num_segments_in_ingredients = len(segment_counts_in_ingredients)
cmap_in_ingredients = ListedColormap(plt.cm.get_cmap('tab20', num_segments_in_ingredients).colors[:num_segments_in_ingredients])

# Plotting Pie Chart for "In Instructions" and "In Ingredients" in a single graph
plt.figure(figsize=(14, 7))  # Set the figure size to be wider for both pie charts

# Create the pie chart for "In Instructions"
plt.subplot(1, 2, 1)
colors_in_instructions = cmap_in_instructions.colors  # Get the distinct colors from the colormap
wedges1, texts1, autotexts1 = plt.pie(
    segment_counts_in_instructions, 
    labels=None,  # Remove labels to use a legend instead
    autopct='%1.1f%%', 
    startangle=90, 
    colors=colors_in_instructions,
    pctdistance=0.85  # Reduce percentage text position
)

# Add a legend for "In Instructions"
plt.legend(
    wedges1, 
    segment_counts_in_instructions.index, 
    title="Instructions Segments", 
    loc="center left", 
    bbox_to_anchor=(1, 0, 0.5, 1), 
    fontsize=10
)

# Adjust text size for readability
plt.setp(autotexts1, size=8)

# Title for "In Instructions"
plt.title('Percentage Distribution of Ingredients Found in Instructions', fontsize=14)

# Create the pie chart for "In Ingredients"
plt.subplot(1, 2, 2)
colors_in_ingredients = cmap_in_ingredients.colors  # Get the distinct colors from the colormap
wedges2, texts2, autotexts2 = plt.pie(
    segment_counts_in_ingredients, 
    labels=None,  # Remove labels to use a legend instead
    autopct='%1.1f%%', 
    startangle=90, 
    colors=colors_in_ingredients,
    pctdistance=0.85  # Reduce percentage text position
)

# Add a legend for "In Ingredients"
plt.legend(
    wedges2, 
    segment_counts_in_ingredients.index, 
    title="Ingredients Segments", 
    loc="center left", 
    bbox_to_anchor=(1, 0, 0.5, 1), 
    fontsize=10
)

# Adjust text size for readability
plt.setp(autotexts2, size=8)

# Title for "In Ingredients"
plt.title('Percentage Distribution of Ingredients Found in Ingredients List', fontsize=14)

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the chart
plt.show()
