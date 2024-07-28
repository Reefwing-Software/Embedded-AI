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

# Select columns to plot
columns_to_plot = ['Voltage', 'Average Voltage', 'Current', 'Average Current', 'Temperature', 'SOC']

# Create a box plot for each selected column
plt.figure(figsize=(12, 6))
data[columns_to_plot].boxplot()
plt.title('Box Plot of Input Features and SOC')
plt.ylabel('Value')
plt.grid(True)
plt.show()