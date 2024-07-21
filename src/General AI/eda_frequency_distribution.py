# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)

# Load the data
data = pd.read_csv(file_path)

# Get columns for which to plot frequency histogram
columns = ['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current', 'SOC']

# Define pastel colors for each feature
colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightskyblue', 'lightpink', 'lightgoldenrodyellow']

# Create subplots for each column
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))
axes = axes.flatten()

# Plot frequency histogram for each column
for i, col in enumerate(columns):
    data[col].hist(bins=50, edgecolor='black', ax=axes[i], color=colors[i], alpha=0.7, label=col)
    axes[i].set_xlabel(col)
    axes[i].set_ylabel('Frequency')
    axes[i].legend()
    axes[i].grid(True)

plt.tight_layout()
plt.show()