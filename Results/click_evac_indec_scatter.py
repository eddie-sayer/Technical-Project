# Import necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load the data
df = pd.read_csv('all_responses.csv')

# Convert the columns to numeric types
df['Clicks'] = pd.to_numeric(df['Clicks'], errors='coerce')
df['EvacuationTime'] = pd.to_numeric(df['EvacuationTime'], errors='coerce')
df['IndecisiveTime'] = pd.to_numeric(df['IndecisiveTime'], errors='coerce')

# Create a figure with two subplots side by side
fig, axs = plt.subplots(ncols=2, figsize=(15, 6))

# Create a scatter plot with regression line for Clicks vs IndecisiveTime
sns.regplot(x='Clicks', y='IndecisiveTime', data=df, ax=axs[0], color='green')
axs[0].set_title('Click Number vs Indecisive Time', fontsize=18)

# Create a scatter plot with regression line for Clicks vs EvacuationTime
sns.regplot(x='Clicks', y='EvacuationTime', data=df, ax=axs[1])
axs[1].set_title('Click Number vs Evacuation Time', fontsize=18)

# Set the labels
for ax in axs:
    ax.set_xlabel('Click Number', fontsize=15)

axs[0].set_ylabel('Indecisive Time (s)', fontsize=15)
axs[1].set_ylabel('Evacuation Time (s)', fontsize=15)

# Show the plot
plt.show()