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

# Calculate the correlation matrix
correlation_matrix = data.corr()

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