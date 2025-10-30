# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=8)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_6")
image_name = 'f06008.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP/eda/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)

# Load the data
data = pd.read_csv(file_path)

# Select columns to plot
columns_to_plot = ['Voltage', 'Average Voltage', 'Current', 'Average Current', 'Temperature', 'SOC']

# Create a box plot for each selected column
plt.figure(figsize=(12, 6))
boxplot = data[columns_to_plot].boxplot(
    patch_artist=True,  # Enables filling the box with color
    boxprops=dict(color='gray', facecolor='lightgray'),  # Color of the box
    whiskerprops=dict(color='black'),  # Color of the whiskers
    capprops=dict(color='gray'),  # Color of the caps
    medianprops=dict(color='black'),  # Color of the median line
    flierprops=dict(markerfacecolor='black', markeredgecolor='darkgray'),  # Color of the outliers
)

# Customize labels and grid in grayscale
plt.ylabel('Value', fontproperties=prop)
plt.grid(True, color='gray', linestyle='--', linewidth=0.7)

# Save the figure
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()