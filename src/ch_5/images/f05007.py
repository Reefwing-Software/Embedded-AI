# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import matplotlib.font_manager as fm

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_5_v6")
image_name = 'f05007.pdf'
image_path = os.path.join(image_folder, image_name)

# Load the data
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_5/eda/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)
data = pd.read_csv(file_path)

# Extract the 'Voltage', 'Current', and 'SOC' columns
voltage_data = data['Voltage']
current_data = data['Current']
soc_data = data['SOC']

# Create subplots for QN plots
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# QN plot for Voltage
res = stats.probplot(voltage_data, dist="norm", plot=axes[0])
axes[0].get_lines()[0].set_color('black')  # Line color
axes[0].get_lines()[1].set_color('darkgray')  # Fit line color
axes[0].set_title('Quantile-normal (QN) plot for voltage data', fontproperties=prop)
axes[0].set_xlabel('Theoretical quantiles', fontproperties=prop)
axes[0].set_ylabel('Sample quantiles', fontproperties=prop)

# QN plot for Current
res = stats.probplot(current_data, dist="norm", plot=axes[1])
axes[1].get_lines()[0].set_color('black')  # Line color
axes[1].get_lines()[1].set_color('darkgray')  # Fit line color
axes[1].set_title('Quantile-normal (QN) plot for current data', fontproperties=prop)
axes[1].set_xlabel('Theoretical quantiles', fontproperties=prop)
axes[1].set_ylabel('Sample quantiles', fontproperties=prop)

# QN plot for SOC
res = stats.probplot(soc_data, dist="norm", plot=axes[2])
axes[2].get_lines()[0].set_color('black')  # Line color
axes[2].get_lines()[1].set_color('darkgray')  # Fit line color
axes[2].set_title('Quantile-normal (QN) plot for SOC data', fontproperties=prop)
axes[2].set_xlabel('Theoretical quantiles', fontproperties=prop)
axes[2].set_ylabel('Sample quantiles', fontproperties=prop)

plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()