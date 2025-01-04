import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Load the data from the CSV file
file_name = "combined_stats.csv"
df = pd.read_csv(file_name)

# Calculate percentages
df['Percentage'] = (df['Ingredients Found in Instructions'] / df['len(ingredients)']) * 100

# Create bins and labels for the new segments
bins = [-1] + list(range(0, 101, 5))  # Bins from -1 to 100 with steps of 5
labels = ['== 0'] + [f'> {i} and <= {i + 5}' for i in range(0, 95, 5)] + ['> 95 and <= 100']

# Categorize into new segments
df['Segment'] = pd.cut(
    df['Percentage'],
    bins=bins,
    labels=labels,
    right=True
)

# Count each segment for the pie chart
segment_counts = df['Segment'].value_counts(sort=False)

# Create a colormap with distinct colors for each segment
num_segments = len(segment_counts)
cmap = ListedColormap(plt.cm.get_cmap('tab20', num_segments).colors[:num_segments])

# Create the pie chart
plt.figure(figsize=(14, 14))  # Increase figure size
colors = cmap.colors  # Get the distinct colors from the colormap

# Create the pie chart
wedges, texts, autotexts = plt.pie(
    segment_counts, 
    labels=None,  # Remove labels to use a legend instead
    autopct='%1.1f%%', 
    startangle=90, 
    colors=colors,
    pctdistance=0.85  # Reduce percentage text position
)

# Add a legend to the side
plt.legend(
    wedges, 
    segment_counts.index, 
    title="Segments", 
    loc="center left", 
    bbox_to_anchor=(1, 0, 0.5, 1), 
    fontsize=10
)

# Adjust text size for readability
plt.setp(autotexts, size=8)

# Title
plt.title('Detailed Percentage Distribution of Ingredients Found in Instructions', fontsize=14)

# Show the chart
plt.show()
