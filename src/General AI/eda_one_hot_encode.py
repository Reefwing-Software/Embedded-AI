# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import pandas as pd
import os

# Load the resampled data
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)
data = pd.read_csv(file_path)

# Define the ranges for Temperature categories (adjusted for every 100th point)
idx0_range = range(0, 184257//100 + 1)
idx10_range = range(184258//100, 337973//100 + 1)
idx25_range = range(337974//100, 510530//100 + 1)
idxN10_range = range(510531//100, 669956//100 + 1)

# Initialize Temperature column with default values
data['Temperature'] = 0

# Assign Temperature values based on the given ranges
data.loc[data.index.isin(idx0_range), 'Temperature'] = 0
data.loc[data.index.isin(idx10_range), 'Temperature'] = 10
data.loc[data.index.isin(idx25_range), 'Temperature'] = 25
data.loc[data.index.isin(idxN10_range), 'Temperature'] = -10

# One-hot encode the Temperature column
data_encoded = pd.get_dummies(data, columns=['Temperature'])

# Save the new DataFrame with one-hot encoded Temperature
new_file_name = 'resampled_training_data_with_temp_encoded.csv'
new_file_path = os.path.join(data_folder, new_file_name)
data_encoded.to_csv(new_file_path, index=False)

print(f"Data with one-hot encoded Temperature saved to {new_file_path}")