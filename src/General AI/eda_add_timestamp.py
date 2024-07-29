# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd

# Load the data
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)
data = pd.read_csv(file_path)

# Add a timestamp column with 100 seconds interval
data['Timestamp'] = pd.date_range(start='2024-01-01', periods=len(data), freq='100S')

# Save the modified dataset
save_file_name = 'resampled_training_data_with_timestamp.csv'
save_file_path = os.path.join(data_folder, save_file_name)
data.to_csv(save_file_path, index=False)

print("Timestamp added with 100 seconds interval. Dataset saved.")