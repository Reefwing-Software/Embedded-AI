# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)

# Load the data
data = pd.read_csv(file_path)

# Select 5 different data points
data_points = data.sample(n=5, random_state=42)

# Variables to plot
categories = ['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current', 'SOC']
num_vars = len(categories)

# Create radar chart
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Compute angles for the radar chart
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

# Function to create radar plot
def create_radar_plot(data_point, color):
    values = data_point[categories].values.flatten().tolist()
    values += values[:1]  # Repeat the first value to close the circular graph
    
    ax.fill(angles, values, color=color, alpha=0.25)
    ax.plot(angles, values, color=color, linewidth=2, label=f'Point {data_point.name}')

# Generate a color map
cmap = get_cmap('tab10')

# Plot each selected data point
for i, data_point in data_points.iterrows():
    create_radar_plot(data_point, cmap(i % cmap.N))

# Add labels
ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)

# Add a legend
plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

plt.show()