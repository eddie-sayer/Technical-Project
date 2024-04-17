# Import necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set label font size
label_font = 15

# Load the data
df = pd.read_csv('all_responses.csv')

# Convert the columns to numeric types
df['IndecisiveTime'] = pd.to_numeric(df['IndecisiveTime'], errors='coerce')

# Create a histogram using seaborn
plt.figure(figsize=(10, 6))
sns.histplot(df['IndecisiveTime'], bins=30, color=sns.light_palette("green")[3], binwidth=1)

# Set the title and labels
plt.title('Distribution of Indecisive Time', fontsize=label_font)
plt.xlabel('Indecisive Time (s)', fontsize=label_font)
plt.ylabel('Frequency', fontsize=label_font)

# Set x-ticks to integers incrementing by 1
plt.xticks(range(int(df['IndecisiveTime'].min()), int(df['IndecisiveTime'].max())+3))

# Show the plot
plt.show()