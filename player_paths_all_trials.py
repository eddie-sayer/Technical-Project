import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import ast

df = pd.read_csv('all_responses.csv')
df2 = pd.read_csv('all_player_paths.csv')

c_indices = []
h_indices = []
a_indices = []
ha_indices = []

click_positions = df['Clicks Positions (player.x, player.y, target_x, target_y)']
treatments = df['Treatment']
collision_positions = df['Collision Positions (player.x, player.y, agent.x, agent.y)']
path_positions = df2.iloc[0:40,1:61]

for i, treatment in enumerate(treatments):
    if treatment == 'C':
        c_indices.append(i)
    elif treatment == 'H':
        h_indices.append(i)
    elif treatment == 'A':
        a_indices.append(i)
    elif treatment == 'HA':
        ha_indices.append(i)

print(c_indices, h_indices, a_indices, ha_indices)

flat_path_positions_C = []
flat_path_positions_H = []
flat_path_positions_A = []
flat_path_positions_HA = []

for index, row in path_positions.iterrows():
    print(index)
    for val in row:
        if not pd.isna(val):
            #print(val)
            tuple_val = ast.literal_eval(val)
            if isinstance(tuple_val, tuple) and len(tuple_val) == 4:
                if index in c_indices:
                    flat_path_positions_C.append((tuple_val[0], tuple_val[1]))
                elif index in h_indices:
                    flat_path_positions_H.append((tuple_val[0], tuple_val[1]))
                elif index in a_indices:
                    flat_path_positions_A.append((tuple_val[0], tuple_val[1]))
                elif index in ha_indices:
                    flat_path_positions_HA.append((tuple_val[0], tuple_val[1]))
                
                #flat_path_positions.append((tuple_val[0], tuple_val[1]))


flat_path_positions_C = [(pos[0], pos[1]) for pos in flat_path_positions_C]
flat_path_positions_H = [(pos[0], pos[1]) for pos in flat_path_positions_H]
flat_path_positions_A = [(pos[0], pos[1]) for pos in flat_path_positions_A]
flat_path_positions_HA = [(pos[0], pos[1]) for pos in flat_path_positions_HA]

np.array(flat_path_positions_C)
np.array(flat_path_positions_H)
np.array(flat_path_positions_A)
np.array(flat_path_positions_HA)

# Merge all the path positions into one list
flat_path_positions_all = flat_path_positions_C + flat_path_positions_H + flat_path_positions_A + flat_path_positions_HA

# Create a single heatmap
fig, ax = plt.subplots(figsize=(10, 10))

# Create a 2D histogram to represent path densities
heatmap, xedges, yedges = np.histogram2d(
    [pos[0] for pos in flat_path_positions_all],  # x coordinates
    [pos[1] for pos in flat_path_positions_all],  # y coordinates
    bins=(90, 75),  # specify the grid size
    range=[[0, 900], [0, 750]]  # specify the range of x and y coordinates
)

# Flatten the heatmap array
flat_heatmap = heatmap.flatten()

# Get the unique values
unique_values = np.unique(flat_heatmap)

# Print the unique values
print(unique_values)

# Set vmax to a value lower than the maximum value
#vmax_value = np.max(heatmap) * (5/18)  # Adjust this value as needed
vmax_value = 10

# Plot the heatmap using Seaborn with a diverging colormap
im = sns.heatmap(heatmap.T, cmap='RdYlBu_r', vmax=vmax_value, ax=ax, cbar=False)  # Using a diverging colormap

# Create a colorbar
cbar = plt.colorbar(im.collections[0], ax=ax)

# Manually set the ticks and labels on the colorbar
cbar.set_ticklabels([])

# Set the title of the subplot
ax.set_title("Player Positions Across all Treatments", fontsize=15)

# Remove the existing x and y axis labels
ax.set_xticklabels([])
ax.set_yticklabels([])

# Move the x-axis to the top of the plot
ax.xaxis.tick_top()

# Manually add the x axis labels
ax.text(0.5, -1.4, str(int(xedges[0])), ha='center', va='center', fontsize=10)
ax.text(len(xedges)-2.4, -1.4, str(int(xedges[-1])), ha='center', va='center', fontsize=10)

# Manually add the y axis labels
ax.text(-1.5, 0.5, str(int(yedges[0])), ha='center', va='center')
ax.text(-2.5, len(yedges)-1.5, str(int(yedges[-1])), ha='center', va='center')

# Manually set the colorbar labels
label_0 = "0"
label_1 = "2"
label_2 = "4"
label_3 = "6"
label_4 = "8"
label_5 = " ≥10"

ax.text(102, 75, label_0, ha='center', va='center', fontsize=10)
ax.text(102, 60, label_1, ha='center', va='center', fontsize=10)
ax.text(102, 45, label_2, ha='center', va='center', fontsize=10)
ax.text(102, 30, label_3, ha='center', va='center', fontsize=10)
ax.text(102, 15, label_4, ha='center', va='center', fontsize=10)
ax.text(102, 0, label_5, ha='center', va='center', fontsize=10)

# Show the plot
plt.tight_layout()
plt.show()