import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import ast

player0_target1 = 1


df = pd.read_csv('all_responses.csv')

click_positions = df['Clicks Positions (player.x, player.y, target_x, target_y)']
flat_data_player = [(pos[0], pos[1]) for row in click_positions for pos in eval(row)]
flat_data_target = [(pos[2], pos[3]) for row in click_positions for pos in eval(row)]

plt.figure(figsize=(10, 8))

if player0_target1 == 0:

    heatmap, xedges, yedges = np.histogram2d(
        [pos[0] for pos in flat_data_player],  # x coordinates
        [pos[1] for pos in flat_data_player],  # y coordinates
        bins=(90, 75),                # specify the grid size
        range=[[0, 900], [0, 750]]      # specify the range of x and y coordinates
    )

    plt.title('Player Position per Click', fontsize=20, y=1.05)

else:
    
    heatmap, xedges, yedges = np.histogram2d(
        [pos[0] for pos in flat_data_target],  # x coordinates
        [pos[1] for pos in flat_data_target],  # y coordinates
        bins=(90, 75),                # specify the grid size
        range=[[0, 900], [0, 750]]      # specify the range of x and y coordinates
    )
    plt.title('Target Click Position', fontsize=20, y=1.05)




ax = sns.heatmap(heatmap.T, cmap='RdYlBu_r',cbar=False, vmax=10)  # Using a diverging colormap# Set the colorbar's outline color and linewidth
# Remove the existing x and y axis labels
ax.set_xticklabels([])
ax.set_yticklabels([])

# Create a colorbar
cbar = plt.colorbar(ax.collections[0])#, ax=ax)

# Manually set the ticks and labels on the colorbar
cbar.set_ticklabels([])

# Move the x-axis to the top of the plot
ax.xaxis.tick_top()

# Manually add the x axis labels
ax.text(0.6, -1.5, str(int(xedges[0])), ha='center', va='center', fontsize=10)
ax.text(len(xedges)-2.4, -1.5, str(int(xedges[-1])), ha='center', va='center', fontsize=10)

# Manually add the y axis labels
ax.text(-1.75, 0.6, str(int(yedges[0])), ha='center', va='center')
ax.text(-2.7, len(yedges)-1.3, str(int(yedges[-1])), ha='center', va='center')

# Manually set the colorbar labels
label_0 = "0"
label_1 = "2"
label_2 = "4"
label_3 = "6"
label_4 = "8"
label_5 = " ≥10"

ax.text(103, 75, label_0, ha='center', va='center', fontsize=10)
ax.text(103, 60, label_1, ha='center', va='center', fontsize=10)
ax.text(103, 45, label_2, ha='center', va='center', fontsize=10)
ax.text(103, 30, label_3, ha='center', va='center', fontsize=10)
ax.text(103, 15, label_4, ha='center', va='center', fontsize=10)
ax.text(103, 0, label_5, ha='center', va='center', fontsize=10)

#cbar = ax.collections[0].colorbar
#cbar.outline.set_edgecolor('black')
#cbar.outline.set_linewidth(1)
plt.show()