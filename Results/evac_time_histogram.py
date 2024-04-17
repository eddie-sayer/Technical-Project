# Import necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set label font size
label_font = 15

# Load the data
df = pd.read_csv('all_responses.csv')

# Convert the columns to numeric types
df['EvacuationTime'] = pd.to_numeric(df['EvacuationTime'], errors='coerce')

# Find the maximum evacuation time
min_evac_time = df['EvacuationTime'].min()
max_evac_time = df['EvacuationTime'].max()

print(f"The minimum evacuation time is {min_evac_time} seconds.")
print(f"The maximum evacuation time is {max_evac_time} seconds.")

# Calculate the bin edges
bin_edges = range(26, int(df['EvacuationTime'].max())+2, 2)

# Create a histogram using seaborn
plt.figure(figsize=(10, 6))
sns.histplot(df['EvacuationTime'], bins=bin_edges, color=sns.light_palette("blue")[3])

# Set the title and labels
plt.title('Distribution of Evacuation Time', fontsize=label_font)
plt.xlabel('Evacuation Time (s)', fontsize=label_font)
plt.ylabel('Frequency', fontsize=label_font)

# Set x-ticks to align with every new bin
plt.xticks(bin_edges)

plt.show()