# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_5_v6")
image_name = 'f05004.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_5/eda/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)

# Load the data
data = pd.read_csv(file_path)

# Get columns for which to plot frequency histogram
columns = ['Voltage', 'Current', 'Temperature', 'Average voltage', 'Average current', 'SOC']

# Define pastel colors for each feature
# colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightskyblue', 'lightpink', 'lightgoldenrodyellow']

# Create subplots for each column
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))
axes = axes.flatten()

# Plot frequency histogram for each column
for i, col in enumerate(columns):
    data[col].hist(bins=50, edgecolor='black', ax=axes[i], color='lightgray', alpha=0.9, label=col)
    axes[i].set_xlabel(col, fontproperties=prop)
    axes[i].set_ylabel('Frequency', fontproperties=prop)
    axes[i].legend(prop=prop)
    axes[i].grid(True)

plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()