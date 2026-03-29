# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the training data
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_5/eda/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)
data = pd.read_csv(file_path)

# Initialize the StandardScaler
scaler = StandardScaler()

# Select the columns to standardise (excluding non-numeric columns)
columns_to_standardise = data.select_dtypes(include=[float, int]).columns

# Standardise the selected columns
data[columns_to_standardise] = scaler.fit_transform(data[columns_to_standardise])

# Save the standardized data to a new CSV file
new_file_name = 'standardised_training_data.csv'
new_file_path = os.path.join(data_folder, new_file_name)
data.to_csv(new_file_path, index=False)

print(f"Standardised data saved to {new_file_path}")