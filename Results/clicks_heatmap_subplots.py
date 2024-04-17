import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import ast

s = 1
r = 0

df = pd.read_csv('all_responses.csv')

click_positions = df['Clicks Positions (player.x, player.y, target_x, target_y)']
flat_data_player = [(pos[0], pos[1]) for row in click_positions for pos in eval(row)]
flat_data_target = [(pos[2], pos[3]) for row in click_positions for pos in eval(row)]

# CLICKS POSITIONS - Player position
# Create a 2D histogram to represent click densities
heatmap_player, xedges_player, yedges_player = np.histogram2d(
    [pos[0] for pos in flat_data_player],  # x coordinates
    [pos[1] for pos in flat_data_player],  # y coordinates
    bins=(90, 75),                # specify the grid size
    range=[[0, 900], [0, 750]]      # specify the range of x and y coordinates
)

heatmap_target, xedges_target, yedges_target = np.histogram2d(
    [pos[0] for pos in flat_data_target],  # x coordinates
    [pos[1] for pos in flat_data_target],  # y coordinates
    bins=(90, 75),                # specify the grid size
    range=[[0, 900], [0, 750]]      # specify the range of x and y coordinates
)

#unique_values = []
# Flatten the heatmap array and find the unique values
#unique_values.extend(np.unique(heatmap))

# Show the unique values
#print(unique_values)
fig1, ax1 = plt.subplots(1, 2, figsize=(10 * s, 8 * s))

# Show the plot
#plt.figure(figsize=(10, 8))
# Player heatmap
ax = sns.heatmap(heatmap_player.T, cmap='RdYlBu_r',cbar=False, vmax=10, ax=ax1, square=True)  # Using a diverging colormap
ax.set_title('Player Position per Click', fontsize=15, y=1.05)
#ax = sns.heatmap(heatmap.T, cmap='RdYlBu_r',cbar=True, vmax=10)  # Using a diverging colormap
"""
# Set the colorbar's outline color and linewidth
cbar = ax.collections[0].colorbar
cbar.outline.set_edgecolor('black')
cbar.outline.set_linewidth(1)
"""
# Remove the existing x and y axis labels
ax.set_xticklabels([])
ax.set_yticklabels([])

# Move the x-axis to the top of the plot
ax.xaxis.tick_top()

# Manually add the x axis labels
ax.text(0.5, -1.5, str(int(xedges_player[0])), ha='center', va='center', fontsize=10)
ax.text(len(xedges_player)-2.3, -1.5, str(int(xedges_player[-1])), ha='center', va='center', fontsize=10)

# Manually add the y axis labels
ax.text(-1.75, 0.6, str(int(yedges_player[0])), ha='center', va='center')
ax.text(-2.9, len(yedges_player)-1.3, str(int(yedges_player[-1])), ha='center', va='center')

# Create colorbar for the first subplot
cbar_ax = fig1.add_axes([0.49, 0.215, 0.015, 0.5595])
cbar = fig1.colorbar(ax1.collections[0], cax=cbar_ax, orientation='vertical')

# Remove the existing colorbar labels
cbar.ax.set_yticklabels([])

# Manually add the colorbar labels
cbar.ax.text(1.5, -0.01, '0', ha='center', va='center')
cbar.ax.text(1.5, 1.97, '2', ha='center', va='center')
cbar.ax.text(1.5, 3.96 , '4', ha='center', va='center')
cbar.ax.text(1.5, 5.97, '6', ha='center', va='center')
cbar.ax.text(1.5, 7.98, '8', ha='center', va='center')
cbar.ax.text(1.9, 9.98, '≥10', ha='center', va='center')


# Target heatmap
fig2, ax2 = plt.subplots(figsize=(10 * s, 8 * s))
ax = sns.heatmap(heatmap_target.T, cmap='RdYlBu_r',cbar=False, vmax=10, ax=ax2, square=True)  # Using a diverging colormap
ax.set_title('Target Click Position', fontsize=15, y=1.05)

# Create colorbar for the second subplot
cbar_ax = fig2.add_axes([0.913, 0.215, 0.015, 0.5595])
cbar = fig2.colorbar(ax2.collections[0], cax=cbar_ax, orientation='vertical')

#Remove the existing colorbar labels
cbar.ax.set_yticklabels([])

# Manually add the colorbar labels
cbar.ax.text(1.5 + r, -0.01, '0', ha='center', va='center')
cbar.ax.text(1.5 + r, 1.97, '2', ha='center', va='center')
cbar.ax.text(1.5 + r, 3.96 , '4', ha='center', va='center')
cbar.ax.text(1.5 + r, 5.97, '6', ha='center', va='center')
cbar.ax.text(1.5 + r, 7.98, '8', ha='center', va='center')
cbar.ax.text(1.9 + r, 9.98, '≥10', ha='center', va='center')

"""
# Set the colorbar's outline color and linewidth
cbar = ax.collections[0].colorbar
cbar.outline.set_edgecolor('black')
cbar.outline.set_linewidth(1)
"""
# Remove the existing x and y axis labels
ax.set_xticklabels([])
ax.set_yticklabels([])

# Move the x-axis to the top of the plot
ax.xaxis.tick_top()

# Manually add the x axis labels
ax.text(0.5, -1.5, str(int(xedges_player[0])), ha='center', va='center', fontsize=10)
ax.text(len(xedges_player)-2.3, -1.5, str(int(xedges_player[-1])), ha='center', va='center', fontsize=10)

# Manually add the y axis labels
ax.text(-1.75, 0.6, str(int(yedges_player[0])), ha='center', va='center')
ax.text(-2.9, len(yedges_player)-1.3, str(int(yedges_player[-1])), ha='center', va='center')

plt.show()