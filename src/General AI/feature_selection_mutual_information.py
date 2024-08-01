# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
from sklearn.feature_selection import mutual_info_regression

# Load the standardized data
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'standardised_training_data.csv'
file_path = os.path.join(data_folder, file_name)
data = pd.read_csv(file_path)

# Separate the features and the target
X = data.drop(columns=['SOC'])
y = data['SOC']

# Perform Mutual Information Regression
mi_scores = mutual_info_regression(X, y, random_state=42)

# Create a DataFrame to store the results
mi_results = pd.DataFrame({
    'Feature': X.columns,
    'Mutual Information Score': mi_scores
})

# Rank the features based on Mutual Information score
mi_results = mi_results.sort_values(by='Mutual Information Score', ascending=False)
print(mi_results)

# Save the results to a new CSV file
# results_file_name = 'mutual_information_feature_ranking.csv'
# results_file_path = os.path.join(data_folder, results_file_name)
# mi_results.to_csv(results_file_path, index=False)

# print(f"Mutual Information feature ranking saved to {results_file_path}")