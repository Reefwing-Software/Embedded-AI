# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd

# Load the standardized data
data_folder = os.path.expanduser("~/Documents/GitHub/NSP/eda/Preprocessed")
file_name = 'standardised_training_data.csv'
file_path = os.path.join(data_folder, file_name)
data = pd.read_csv(file_path)
target_column = 'SOC'
correlation_matrix = data.corr()

# Identify features with high correlation to the target variable
target_correlation = correlation_matrix[target_column].abs().sort_values(ascending=False)
print("Correlation of features with the target variable:\n", target_correlation)

# Set a threshold to filter out low correlations (e.g., 0.1)
correlation_threshold = 0.1
selected_features = target_correlation[target_correlation > correlation_threshold].index

print("\nSelected features with correlation above the threshold:\n", selected_features)

# Print out the correlations for the specified pairs of features
pairs = [
    ('Voltage', 'Current'),
    ('Voltage', 'Temperature'),
    ('Voltage', 'Average Voltage'),
    ('Current', 'Temperature'),
    ('Current', 'Average Current')
]

print("Correlation between specified pairs of features:\n")
for pair in pairs:
    feature1, feature2 = pair
    correlation = correlation_matrix.loc[feature1, feature2]
    print(f"Correlation between {feature1} and {feature2}: {correlation:.4f}")