# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
from sklearn.feature_selection import chi2
from sklearn.preprocessing import MinMaxScaler

# Load the standardized data
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)
data = pd.read_csv(file_path)

# Separate the features and the target
X = data.drop(columns=['SOC'])
y = data['SOC']

# Perform the Chi-Square test
chi2_scores, p_values = chi2(X, y)

# Create a DataFrame to store the results
chi2_results = pd.DataFrame({
    'Feature': X.columns,
    'Chi2 Score': chi2_scores,
    'p-value': p_values
})

# Rank the features based on Chi2 score
chi2_results = chi2_results.sort_values(by='Chi2 Score', ascending=False)

# Display the ranked features
print(chi2_results)

# Save the results to a new CSV file
# results_file_name = 'chi2_feature_ranking.csv'
# results_file_path = os.path.join(data_folder, results_file_name)
# chi2_results.to_csv(results_file_path, index=False)

# print(f"Chi-Square feature ranking saved to {results_file_path}")