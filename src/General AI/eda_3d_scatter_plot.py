# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)

# Load the data
data = pd.read_csv(file_path)

# Select relevant variables for the 3D scatter plot
x = data['Voltage']
y = data['Current']
z = data['SOC']

# Create 3D scatter plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

sc = ax.scatter(x, y, z, c=z, cmap='viridis', alpha=0.7)

ax.set_title('3D Scatter Plot of Voltage, Current, and SOC')
ax.set_xlabel('Voltage')
ax.set_ylabel('Current')
ax.set_zlabel('SOC')

# Add a color bar to show SOC values
cbar = plt.colorbar(sc)
cbar.set_label('SOC')

plt.show()