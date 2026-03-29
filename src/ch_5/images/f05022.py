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
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_5_v6")
image_name = 'f05022.pdf'
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
current_data = data[['Current']]

# Range Check: Identify outliers based on expected range of [0, 1]
range_outliers = (data['Current'] < 0) | (data['Current'] > 1)

# Rate of Change: Calculate the rate of change and identify significant deviations
rate_of_change = data['Current'].diff().abs()
roc_threshold = rate_of_change.quantile(0.99)  # Define threshold as the 99th percentile
roc_outliers = rate_of_change > roc_threshold

# Temperature Correlation: Check for deviations from expected temperature-current relationship
# For simplicity, assume a linear relationship and use a rolling window correlation
rolling_window = 50
temp_corr = data['Current'].rolling(rolling_window).corr(data['Temperature'])
temp_corr_threshold = 0.5  # Define threshold for correlation
temp_corr_outliers = temp_corr.abs() < temp_corr_threshold

# Combine all outliers
combined_outliers = range_outliers | roc_outliers | temp_corr_outliers

# Filter the dataset to remove outliers
cleaned_data = data[~combined_outliers]

# Count the number of outliers
num_outliers_before = count_outliers(current_data)
num_outliers_after = count_outliers(cleaned_data['Current'])

# Print the number of outliers before and after
print(f"Number of outliers before removal: {num_outliers_before}")
print(f"Number of outliers after removal: {num_outliers_after}")

# Create subplots for box plots before and after removing anomalies
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Box plot for Current before removing anomalies
axes[0].boxplot(data['Current'], vert=False, patch_artist=True,
                boxprops=dict(facecolor='lightgray', color='darkgray'),
                whiskerprops=dict(color='darkgray'),
                capprops=dict(color='darkgray'),
                medianprops=dict(color='black'),
                flierprops=dict(markerfacecolor='darkgray', markeredgecolor='darkgray'))
axes[0].set_title('Box plot of current data (before removing anomalies)', fontproperties=prop, color='black')
axes[0].set_xlabel('Current', fontproperties=prop, color='black')

# Box plot for Current after removing anomalies
axes[1].boxplot(cleaned_data['Current'], vert=False, patch_artist=True,
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

# Save the cleaned dataset
save_file_name = 'cleaned_resampled_training_data.csv'
save_file_path = os.path.join(data_folder, save_file_name)
cleaned_data.to_csv(save_file_path, index=False)

print("Anomalies removed and cleaned dataset saved.")