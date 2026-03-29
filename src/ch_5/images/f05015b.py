# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from mpl_toolkits.mplot3d import Axes3D

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_5_v6")
image_name = 'f05015b.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_5/eda/Preprocessed")
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

# Use a grayscale colormap
sc = ax.scatter(x, y, z, c=z, cmap='Greys', alpha=0.7)

# Apply the custom font properties to the axis labels
ax.set_xlabel('Voltage', fontproperties=prop, color='black')
ax.set_ylabel('Current', fontproperties=prop, color='black')
ax.set_zlabel('SOC', fontproperties=prop, color='black')

# Add a color bar to show SOC values in grayscale
cbar = plt.colorbar(sc)
cbar.set_label('SOC', fontproperties=prop, color='black')

# Set the desired view angle (you can adjust these values based on your preference)
ax.view_init(elev=10, azim=-70)

# Save the figure
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()