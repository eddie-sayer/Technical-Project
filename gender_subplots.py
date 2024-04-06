import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

label_font = 15

df = pd.read_csv('all_responses.csv')

# Convert the columns to numeric types
df['EvacuationTime'] = pd.to_numeric(df['EvacuationTime'], errors='coerce')
df['IndecisiveTime'] = pd.to_numeric(df['IndecisiveTime'], errors='coerce')
df['Clicks'] = pd.to_numeric(df['Clicks'], errors='coerce')
df['Collisions'] = pd.to_numeric(df['Collisions'], errors='coerce')

# Set the style of the plot
sns.set(style="whitegrid")

# Create a 2x2 grid of subplots
fig, axs = plt.subplots(2, 2)

# Create the boxplots
sns.boxplot(x='Gender', y='EvacuationTime', data=df, ax=axs[0, 0], whis=100, flierprops={'marker': 'x'}, color=sns.light_palette("blue")[3])
axs[0, 0].set_xlabel('Gender', fontsize=label_font)
axs[0, 0].set_ylabel('Evacuation Time (s)', fontsize=label_font)
axs[0, 0].xaxis.set_tick_params(labelsize=label_font)
axs[0, 0].yaxis.set_tick_params(labelsize=label_font)

sns.boxplot(x='Gender', y='IndecisiveTime', data=df, ax=axs[0, 1], whis=100, flierprops={'marker': 'x'}, color=sns.light_palette("green")[3])
axs[0, 1].set_xlabel('Gender', fontsize=label_font)
axs[0, 1].set_ylabel('Indecisive Time (s)', fontsize=label_font)
axs[0, 1].xaxis.set_tick_params(labelsize=label_font)
axs[0, 1].yaxis.set_tick_params(labelsize=label_font)

sns.boxplot(x='Gender', y='Clicks', data=df, ax=axs[1, 0], whis=100, flierprops={'marker': 'x'}, color=sns.light_palette("red")[3])
axs[1, 0].set_xlabel('Gender', fontsize=label_font)
axs[1, 0].set_ylabel('Click number', fontsize=label_font)
axs[1, 0].xaxis.set_tick_params(labelsize=label_font)
axs[1, 0].yaxis.set_tick_params(labelsize=label_font)

sns.boxplot(x='Gender', y='Collisions', data=df, ax=axs[1, 1], whis=100, flierprops={'marker': 'x'}, color=sns.light_palette("purple")[3])
axs[1, 1].set_xlabel('Gender', fontsize=label_font)
axs[1, 1].set_ylabel('Collision number', fontsize=label_font)
axs[1, 1].xaxis.set_tick_params(labelsize=label_font)
axs[1, 1].yaxis.set_tick_params(labelsize=label_font)

# Add a title to the plot
fig.suptitle('Distribution of Responses Separated by Gender', fontsize=20)

# Adjust the space between the subplots
plt.subplots_adjust(hspace = 0.3)

# Show the plot
plt.show()