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
image_name = 'f05012.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_5/eda/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)

# Load the data
data = pd.read_csv(file_path)

# Create subplots for scatter plots
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 12))

# Scatter plot SOC vs Voltage
axes[0, 0].scatter(data['Voltage'], data['SOC'], alpha=0.5, color='darkgray')
axes[0, 0].set_title('SOC vs voltage', fontproperties=prop)
axes[0, 0].set_xlabel('Voltage', fontproperties=prop)
axes[0, 0].set_ylabel('SOC', fontproperties=prop)
axes[0, 0].grid(True)

# Scatter plot SOC vs Current
axes[0, 1].scatter(data['Current'], data['SOC'], alpha=0.5, color='darkgray')
axes[0, 1].set_title('SOC vs current', fontproperties=prop)
axes[0, 1].set_xlabel('Current', fontproperties=prop)
axes[0, 1].set_ylabel('SOC', fontproperties=prop)
axes[0, 1].grid(True)

# Scatter plot Voltage vs Current
axes[0, 2].scatter(data['Voltage'], data['Current'], alpha=0.5, color='darkgray')
axes[0, 2].set_title('Voltage vs current', fontproperties=prop)
axes[0, 2].set_xlabel('Voltage', fontproperties=prop)
axes[0, 2].set_ylabel('Current', fontproperties=prop)
axes[0, 2].grid(True)

# Scatter plot SOC vs Average Voltage
axes[1, 0].scatter(data['Average Voltage'], data['SOC'], alpha=0.5, color='darkgray', label='Average voltage')
axes[1, 0].set_title('SOC vs average voltage', fontproperties=prop)
axes[1, 0].set_xlabel('Average voltage', fontproperties=prop)
axes[1, 0].set_ylabel('SOC', fontproperties=prop)
axes[1, 0].grid(True)

# Scatter plot SOC vs Average Current
axes[1, 1].scatter(data['Average Current'], data['SOC'], alpha=0.5, color='darkgray', label='Average current')
axes[1, 1].set_title('SOC vs average current', fontproperties=prop)
axes[1, 1].set_xlabel('Average current', fontproperties=prop)
axes[1, 1].set_ylabel('SOC', fontproperties=prop)
axes[1, 1].grid(True)

# Scatter plot SOC vs Temperature
axes[1, 2].scatter(data['Temperature'], data['SOC'], alpha=0.5, color='darkgray')
axes[1, 2].set_title('SOC vs temperature', fontproperties=prop)
axes[1, 2].set_xlabel('Temperature', fontproperties=prop)
axes[1, 2].set_ylabel('SOC', fontproperties=prop)
axes[1, 2].grid(True)

plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()