# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Function to count outliers using IQR method
def count_outliers(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).sum()
    return outliers

# Load the data
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)
data = pd.read_csv(file_path)

# Extract the 'Current' column
current_data = data[['Current']]

# Fit the Isolation Forest model
iso_forest = IsolationForest(contamination=0.1, random_state=42)
iso_forest.fit(current_data)

# Predict anomalies
anomalies = iso_forest.predict(current_data)

# Remove anomalies
current_data_clean = current_data[anomalies == 1]

# Count the number of outliers
num_outliers_before = count_outliers(current_data)
num_outliers_after = count_outliers(current_data_clean)

# Print the number of outliers before and after
print(f"Number of outliers before removal: {num_outliers_before}")
print(f"Number of outliers after removal: {num_outliers_after}")

# Create subplots for box plots before and after removing anomalies
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Box plot for Current before removing anomalies
axes[0].boxplot(current_data, vert=False)
axes[0].set_title('Box Plot of Current Data (Before Removing Anomalies)')
axes[0].set_xlabel('Current')

# Box plot for Current after removing anomalies
axes[1].boxplot(current_data_clean, vert=False)
axes[1].set_title('Box Plot of Current Data (After Removing Anomalies)')
axes[1].set_xlabel('Current')

plt.tight_layout()
plt.show()