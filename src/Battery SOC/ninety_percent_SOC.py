# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, max_error
from sklearn.preprocessing import StandardScaler
from custom_kernels import ExponentialKernel, custom_optimizer

# Custom loss functions
def trimmed_rmse(y_true, y_pred):
    y_pred_trimmed = np.clip(y_pred, 0, 1)
    return np.sqrt(mean_squared_error(y_true, y_pred_trimmed))

def trimmed_max_abs_error(y_true, y_pred):
    y_pred_trimmed = np.clip(y_pred, 0, 1)
    return max_error(y_true, y_pred_trimmed)

# Calculate RMSE up to 0.9 SOC
def rmse_up_to_threshold(y_true, y_pred, threshold=0.5):
    mask = y_true <= threshold
    y_true_filtered = y_true[mask]
    y_pred_filtered = y_pred[mask]
    return trimmed_rmse(y_true_filtered, y_pred_filtered)

# Define file paths
preprocessed_folder = os.path.expanduser("~/Documents/GitHub/Embedded-AI/data/LGHG2@n10C_to_25degC/Preprocessed")
model_folder = os.path.expanduser("~/Documents/GitHub/Embedded-AI/data/LGHG2@n10C_to_25degC/Model")
model_file = os.path.join(model_folder, 'best_gpr_model.pkl')

# Load the best model
best_gpr_model = joblib.load(model_file)

# Load the test data
test_files = [
    "resampled_test_data_n10degC.csv",
    "resampled_test_data_0degC.csv",
    "resampled_test_data_10degC.csv",
    "resampled_test_data_25degC.csv"
]

test_data = [pd.read_csv(f"{preprocessed_folder}/{file}") for file in test_files]

# Extract features and target variable for each test set
X_test_list = [df[['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current']] for df in test_data]
y_test_list = [df['SOC'] for df in test_data]

# Load the training data for scaling
train_file = os.path.join(preprocessed_folder, 'resampled_training_data.csv')
train_df = pd.read_csv(train_file)
X_train = train_df[['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current']]

# Standardize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Convert scaled training data back to DataFrame to keep feature names
X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)

# Standardize the test data
X_test_scaled_list = [pd.DataFrame(scaler.transform(X), columns=X.columns) for X in X_test_list]

# Calculate RMSE and Max Absolute Error for each temperature
rmse_list = []
max_abs_error_list = []
rmse_up_to_0_9_list = []

for X_test_scaled, y_test in zip(X_test_scaled_list, y_test_list):
    y_pred = best_gpr_model.predict(X_test_scaled)
    rmse_list.append(trimmed_rmse(y_test, y_pred))
    max_abs_error_list.append(trimmed_max_abs_error(y_test, y_pred))
    rmse_up_to_0_9_list.append(rmse_up_to_threshold(y_test, y_pred))

# Plotting
temperatures = ["-10°C", "0°C", "10°C", "25°C"]

plt.figure(figsize=(18, 6))

plt.subplot(1, 3, 1)
plt.bar(temperatures, rmse_list, color='blue')
plt.title('RMSE for Each Ambient Temperature')
plt.xlabel('Ambient Temperature')
plt.ylabel('RMSE')

plt.subplot(1, 3, 2)
plt.bar(temperatures, max_abs_error_list, color='red')
plt.title('Max Absolute Error for Each Ambient Temperature')
plt.xlabel('Ambient Temperature')
plt.ylabel('Max Absolute Error')

plt.subplot(1, 3, 3)
plt.bar(temperatures, rmse_up_to_0_9_list, color='green')
plt.title('RMSE up to 0.9 SOC for Each Ambient Temperature')
plt.xlabel('Ambient Temperature')
plt.ylabel('RMSE up to 0.9 SOC')

plt.tight_layout()
plt.show()