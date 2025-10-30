# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=10)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_6")
image_name = 'f06016.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP/eda/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)

# Load the data
data = pd.read_csv(file_path)

# Compute the correlation matrix
corr = data[['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current', 'SOC']].corr()

# Generate a heatmap
plt.figure(figsize=(12, 12))
sns.heatmap(corr, annot=True, cmap='Greys', vmin=-1, vmax=1, annot_kws={"size": 10, "fontproperties": prop})
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()