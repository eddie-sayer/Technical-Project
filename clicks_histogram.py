# Import necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set label font size
label_font = 15

# Load the data
df = pd.read_csv('all_responses.csv')

# Convert the columns to numeric types
df['Clicks'] = pd.to_numeric(df['Clicks'], errors='coerce')

# Find the maximum click number
min_evac_time = df['Clicks'].min()
max_evac_time = df['Clicks'].max()

print(f"The minimum click number is {min_evac_time} seconds.")
print(f"The maximum click number is {max_evac_time} seconds.")

# Calculate the bin edges
bin_edges = range(0, int(df['Clicks'].max())+5, 5)

# Create a histogram using seaborn
plt.figure(figsize=(10, 6))
sns.histplot(df['Clicks'], bins=bin_edges, color=sns.light_palette("red")[3])

# Set the title and labels
plt.title('Distribution of Click Number', fontsize=label_font)
plt.xlabel('Click Number', fontsize=label_font)
plt.ylabel('Frequency', fontsize=label_font)

# Set x-ticks to align with every new bin
plt.xticks(bin_edges)

# Set the limits of the x-axis
plt.xlim([0, max(bin_edges)])

# Set x-ticks to integers incrementing by 1
#plt.xticks(range(int(df['Clicks'].min()), int(df['Clicks'].max())+1))

# Show the plot
plt.show()