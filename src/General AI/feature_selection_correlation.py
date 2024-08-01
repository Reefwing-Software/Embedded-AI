# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import pandas as pd
import os

# Load the standardized data
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'standardised_training_data.csv'
file_path = os.path.join(data_folder, file_name)
data = pd.read_csv(file_path)

# Assuming the target column is named 'target_column'
target_column = 'SOC'

# Calculate the correlation matrix
correlation_matrix = data.corr()

# Identify features with high correlation to the target variable
target_correlation = correlation_matrix[target_column].abs().sort_values(ascending=False)

# Display the correlation of features with the target variable
print("Correlation of features with the target variable:\n", target_correlation)

# Set a threshold to filter out low correlations (e.g., 0.1)
correlation_threshold = 0.1
selected_features = target_correlation[target_correlation > correlation_threshold].index

# Print the selected features
print("\nSelected features with correlation above the threshold:\n", selected_features)

# Create a new DataFrame with only the selected features
# selected_data = data[selected_features]

# Save the selected features data to a new CSV file
# new_file_name = 'selected_features_data.csv'
# new_file_path = os.path.join(data_folder, new_file_name)
# selected_data.to_csv(new_file_path, index=False)

# print(f"Data with selected features saved to {new_file_path}")