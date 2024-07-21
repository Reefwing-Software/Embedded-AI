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

# Plot frequency histogram for 'Voltage' column
plt.figure(figsize=(10, 6))
data['Voltage'].hist(bins=50, edgecolor='black')
plt.title('Frequency Histogram of Voltage')
plt.xlabel('Voltage')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()