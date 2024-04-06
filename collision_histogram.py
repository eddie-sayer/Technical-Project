# Import necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set label font size
label_font = 15

# Load the data
df = pd.read_csv('all_responses.csv')

# Convert the columns to numeric types
df['Collisions'] = pd.to_numeric(df['Collisions'], errors='coerce')

# Create a histogram using seaborn
plt.figure(figsize=(10, 6))
sns.histplot(df['Collisions'], bins=30, color=sns.light_palette("purple")[3])

# Set the title and labels
plt.title('Distribution of Collision Number', fontsize=label_font)
plt.xlabel('Collision Number', fontsize=label_font)
plt.ylabel('Frequency', fontsize=label_font)

# Set x-ticks to integers incrementing by 1
plt.xticks(range(int(df['Collisions'].min()), int(df['Collisions'].max())+1))

# Show the plot
plt.show()