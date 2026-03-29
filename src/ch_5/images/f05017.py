# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.font_manager as fm

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_5_v6")
image_name = 'f05017.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_5/eda/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)
data = pd.read_csv(file_path)

# Function to count outliers using IQR method
def count_outliers(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).sum()
    return outliers

# Extract the 'Current' column
current_data = data['Current']

# Calculate z-scores
z_scores = np.abs(stats.zscore(current_data))

# Identify anomalies (z-score threshold > 3)
anomalies = np.where(z_scores > 3)

# Remove anomalies
current_data_clean = current_data.drop(anomalies[0])

# Count the number of outliers
num_outliers_before = count_outliers(current_data)
num_outliers_after = count_outliers(current_data_clean)

# Print the number of outliers before and after
print(f"Number of outliers before removal: {num_outliers_before}")
print(f"Number of outliers after removal: {num_outliers_after}")

# Create subplots for box plots before and after removing anomalies
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Box plot for Current before removing anomalies
axes[0].boxplot(current_data, vert=False, patch_artist=True,
                boxprops=dict(facecolor='lightgray', color='darkgray'),
                whiskerprops=dict(color='darkgray'),
                capprops=dict(color='darkgray'),
                medianprops=dict(color='black'),
                flierprops=dict(markerfacecolor='darkgray', markeredgecolor='darkgray'))
axes[0].set_title('Box plot of current data (before removing anomalies)', fontproperties=prop, color='black')
axes[0].set_xlabel('Current', fontproperties=prop, color='black')

# Box plot for Current after removing anomalies
axes[1].boxplot(current_data_clean, vert=False, patch_artist=True,
                boxprops=dict(facecolor='lightgray', color='darkgray'),
                whiskerprops=dict(color='darkgray'),
                capprops=dict(color='darkgray'),
                medianprops=dict(color='black'),
                flierprops=dict(markerfacecolor='darkgray', markeredgecolor='darkgray'))
axes[1].set_title('Box plot of current data (after removing anomalies)', fontproperties=prop, color='black')
axes[1].set_xlabel('Current', fontproperties=prop, color='black')

plt.tight_layout()

# Save the figure
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()