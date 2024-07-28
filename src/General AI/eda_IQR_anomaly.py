# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)
data = pd.read_csv(file_path)

# Extract the 'Current' column
current_data = data['Current']

# Calculate IQR
Q1 = current_data.quantile(0.25)
Q3 = current_data.quantile(0.75)
IQR = Q3 - Q1

# Identify anomalies
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
anomalies = current_data[(current_data < lower_bound) | (current_data > upper_bound)]

# Remove anomalies
current_data_clean = current_data[~current_data.isin(anomalies)]

# Create subplots for box plots before and after removing anomalies
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Box plot for Current before removing anomalies
axes[0].boxplot(current_data, vert=False)
axes[0].set_title('Box Plot of Current Data (Before Removing Anomalies)')
axes[0].set_xlabel('Current')

# Box plot for Current after removing anomalies
axes[1].boxplot(current_data_clean, vert=False)
axes[1].set_title('Box Plot of Current Data (After Removing Anomalies)')
axes[1].set_xlabel('Current')

plt.tight_layout()
plt.show()