import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MultipleLocator

label_font = 15

df = pd.read_csv('all_responses.csv')
route_choice = df['RouteChoice']

# Set the style of the plot
sns.set(style="whitegrid")

# Define the order of the categories
order = df['RouteChoice'].value_counts(ascending=True).index

# Create a color list with a bluer shade for 'B'
colors = ['#FFA040' if route == 'A' else '#6090C0' for route in order]

# Create a countplot with the defined order and colors
sns.countplot(x='RouteChoice', data=df, order=order, palette=colors)

# Set the labels and title
plt.xlabel('Route Choice', fontsize=label_font)
plt.ylabel('Frequency', fontsize=label_font)
plt.title('Route Choice Distribution', fontsize=20)

# Set y-axis to increment by 2  
ax = plt.gca()
ax.yaxis.set_major_locator(MultipleLocator(2))

# Show the plot
plt.show()