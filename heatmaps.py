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
path_positions = df2.iloc[1:40,1:61]

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

flat_path_positions = []

for _, row in path_positions.iterrows():
    for val in row:
        if not pd.isna(val):
            #print(val)
            tuple_val = ast.literal_eval(val)
            if isinstance(tuple_val, tuple) and len(tuple_val) == 4:
                flat_path_positions.append((tuple_val[0], tuple_val[1]))

#print(flat_path_positions)

# Flatten the list of tuples and extract the first two elements of each tuple
flat_data_player = [(pos[0], pos[1]) for row in click_positions for pos in eval(row)]

flat_data_target = [(pos[2], pos[3]) for row in click_positions for pos in eval(row)]   

flat_data_collision = [(pos[0], pos[1]) for row in collision_positions for pos in eval(row)]

#flat_path_positions = [(pos[0], pos[1]) for _, row in path_positions.iterrows() for val in row if pd.notna(val) for pos in ast.literal_eval(val)]# if isinstance(pos, tuple)]
#unique_types = {type(val) for _, row in path_positions.iterrows() for val in row}
#print(unique_types)

#print(flat_path_positions)
"""
# List of tuples for path_positions
path_positions_tuples = []
for _, row in path_positions.iterrows():
    for val in row:
        if not pd.isna(val):
            path_positions_tuples.append((val[0], val[1]))

print(path_positions_tuples)
"""
np.array(flat_data_player)
np.array(flat_data_target)
np.array(flat_data_collision)
np.array(flat_path_positions)

#print(flat_data_player)

"""
# CLICKS POSITIONS

# Player position
# Create a 2D histogram to represent click densities
heatmap, xedges, yedges = np.histogram2d(
    [pos[0] for pos in flat_data_player],  # x coordinates
    [pos[1] for pos in flat_data_player],  # y coordinates
    bins=(90, 75),                # specify the grid size
    range=[[0, 900], [0, 750]]      # specify the range of x and y coordinates
)
"""
"""
# Target position
# Create a 2D histogram to represent click densities
heatmap, xedges, yedges = np.histogram2d(
    [pos[0] for pos in flat_data_target],  # x coordinates
    [pos[1] for pos in flat_data_target],  # y coordinates
    bins=(90, 75),                # specify the grid size
    range=[[0, 900], [0, 750]]      # specify the range of x and y coordinates
)
"""
#"""
# COLLISION POSITIONS
# Create a 2D histogram to represent click densities
heatmap, xedges, yedges = np.histogram2d(
    [pos[0] for pos in flat_data_collision],  # x coordinates
    [pos[1] for pos in flat_data_collision],  # y coordinates
    bins=(90, 75),                # specify the grid size
    range=[[0, 900], [0, 750]]      # specify the range of x and y coordinates
)
#"""
"""
# PLAYER PATHS

# Player position
# Create a 2D histogram to represent click densities
heatmap, xedges, yedges = np.histogram2d(
    [pos[0] for pos in flat_path_positions],  # x coordinates
    [pos[1] for pos in flat_path_positions],  # y coordinates
    bins=(90, 75),                # specify the grid size
    range=[[0, 900], [0, 750]]      # specify the range of x and y coordinates
)
"""
# Find the maximum value in the heatmap data
max_value = np.max(heatmap)

# Set vmax to a value lower than the maximum value
vmax_value = max_value * 0.2  # Adjust this value as needed

# Plot the heatmap using Seaborn with a diverging colormap
sns.heatmap(heatmap.T, cmap='RdYlBu_r', vmax=vmax_value)  # Using a diverging colormap

plt.show()