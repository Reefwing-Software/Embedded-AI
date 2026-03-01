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
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_6")
image_name = 'f06011.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP/eda/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)

# Load the data
data = pd.read_csv(file_path)

# Create a time column based on the assumption that each data point is 1 second apart
data['Time'] = data.index

# Plot Current vs Time
plt.figure(figsize=(15, 6))
plt.plot(data['Time'], data['Voltage'], color='darkgray', label='Voltage')
plt.xlabel('Time (seconds)', fontproperties=prop)
plt.ylabel('Voltage', fontproperties=prop)
plt.grid(True)
plt.legend(prop=prop)  # Apply font to legend
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()