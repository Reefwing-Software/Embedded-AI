# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the training data
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)
data = pd.read_csv(file_path)

# Initialize the StandardScaler
scaler = StandardScaler()

# Select the columns to standardize (excluding non-numeric columns)
columns_to_standardize = data.select_dtypes(include=[float, int]).columns

# Standardize the selected columns
data[columns_to_standardize] = scaler.fit_transform(data[columns_to_standardize])

# Save the standardized data to a new CSV file
new_file_name = 'standardized_training_data.csv'
new_file_path = os.path.join(data_folder, new_file_name)
data.to_csv(new_file_path, index=False)

print(f"Standardized data saved to {new_file_path}")