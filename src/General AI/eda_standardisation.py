# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os, time
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Start the timer for the complete script
start_time = time.time()

# Load the training data
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)
data = pd.read_csv(file_path)

# Initialize the StandardScaler
scaler = StandardScaler()

# Select the columns to standardise (excluding non-numeric columns)
columns_to_standardise = data.select_dtypes(include=[float, int]).columns

# Standardize the selected columns
data[columns_to_standardise] = scaler.fit_transform(data[columns_to_standardise])

# Check if the standardisation has been successful
means = data[columns_to_standardise].mean()
stds = data[columns_to_standardise].std()

print("Means after standardisation:\n", means)
print("Standard deviations after standardisation:\n", stds)

# Save the standardised data to a new CSV file
new_file_name = 'standardised_training_data.csv'
new_file_path = os.path.join(data_folder, new_file_name)
data.to_csv(new_file_path, index=False)

print(f"Standardised data saved to {new_file_path}")

# Print the elapsed time for standardisation
total_elapsed_time = time.time() - start_time
total_minutes, total_seconds = divmod(total_elapsed_time, 60)
print(f"Total script execution time: {int(total_minutes)} minutes and {total_seconds:.2f} seconds")
