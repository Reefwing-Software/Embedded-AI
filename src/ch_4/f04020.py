# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils.validation import check_array
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.gaussian_process.kernels import Kernel, Hyperparameter
from scipy.optimize import fmin_l_bfgs_b

# Define the hyperparameters in a configuration dictionary for Trial 6
config = {
    'trial': 6,
    'initial_constant_value': 0.079056,
    'constant_bounds': (0.01, 1.0),
    'initial_length_scales': [0.01, 0.05, 0.1],
    'length_scale_bounds': (0.01, 1.0),
    'max_iter': 30000,
    'n_restarts_optimizer': 15,
    'cv_folds': 5,
    'standardize': True
}

class ExponentialKernel(Kernel):
    def __init__(self, length_scale, length_scale_bounds):
        self.length_scale = length_scale
        self.length_scale_bounds = length_scale_bounds

    @property
    def hyperparameter_length_scale(self):
        return Hyperparameter("length_scale", "numeric", self.length_scale_bounds)

    def __call__(self, X, Y=None, eval_gradient=False):
        X = check_array(X)
        if Y is None:
            Y = X
        dists = np.sqrt(np.sum((X[:, np.newaxis, :] - Y[np.newaxis, :, :]) ** 2, axis=2))
        K = np.exp(-dists / self.length_scale)
        
        if eval_gradient:
            if not self.hyperparameter_length_scale.fixed:
                length_scale_gradient = (dists / (self.length_scale ** 2)) * K
                return K, np.expand_dims(length_scale_gradient, axis=2)
            else:
                return K, np.empty((X.shape[0], X.shape[0], 0))
        return K

    def diag(self, X):
        return np.ones(X.shape[0])

    def is_stationary(self):
        return True

# Custom optimizer function to include max_iter
def custom_optimizer(obj_func, initial_theta, bounds):
    result = fmin_l_bfgs_b(obj_func, initial_theta, bounds=bounds, maxiter=config['max_iter'])
    return result[0], result[1]

# File paths
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/LGHG2@n10C_to_25degC")
preprocessed_folder = os.path.join(data_folder, 'Preprocessed')
model_file = os.path.join(data_folder, 'Model', 'best_gpr_model.pkl')

# Resampled test data file names
test_files = {
    'n10degC': 'resampled_test_data_n10degC.csv',
    '0degC': 'resampled_test_data_0degC.csv',
    '10degC': 'resampled_test_data_10degC.csv',
    '25degC': 'resampled_test_data_25degC.csv'
}

# Performance Metrics Data
datasets = ['n10degC', '0degC', '10degC', '25degC']
rmse = [0.0182, 0.0204, 0.0291, 0.0300]
mae = [0.0083, 0.0121, 0.0169, 0.0179]
r2 = [0.9961, 0.9945, 0.9883, 0.9852]

# Load the saved model
gpr_model = joblib.load(model_file)

# Select a specific temperature band for SOC vs Voltage plot
selected_test_file = test_files['10degC']
test_path = os.path.join(preprocessed_folder, selected_test_file)
test_df = pd.read_csv(test_path)

# Extract features and target
feature_names = ['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current']
X_test = test_df[feature_names]
Y_test = test_df['SOC']

# Predict SOC
predicted_SOC = gpr_model.predict(X_test)
test_df['Predicted_SOC'] = predicted_SOC

# Limit data points for the second plot
test_df_limited = test_df.iloc[:100]

# Create combined plot
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Performance Metrics
x = np.arange(len(datasets))  # Dataset indices
width = 0.25  # Bar width
axes[0].bar(x - width, rmse, width, label='RMSE', color='black')
axes[0].bar(x, mae, width, label='MAE', color='grey')
axes[0].bar(x + width, r2, width, label='R²', color='darkgrey')
axes[0].set_xlabel('Dataset', fontsize=12)
axes[0].set_ylabel('Metrics', fontsize=12)
axes[0].set_title('Performance metrics for resampled test data', fontsize=14)
axes[0].set_xticks(x)
axes[0].set_xticklabels(datasets)
axes[0].legend(fontsize=10)
axes[0].grid(True, linestyle='--', alpha=0.7)

# Plot 2: Voltage vs SOC in Greyscale
axes[1].plot(test_df_limited['SOC'], test_df_limited['Voltage'], label='Actual SOC', color='black', linestyle='-')
axes[1].plot(test_df_limited['Predicted_SOC'], test_df_limited['Voltage'], label='Predicted SOC', color='grey', linestyle='--')
axes[1].set_xlabel('SOC', fontsize=12)
axes[1].set_ylabel('Voltage (V)', fontsize=12)
axes[1].set_title('Voltage vs SOC for 10degC dataset', fontsize=14)
axes[1].legend(fontsize=10)
axes[1].grid(True, linestyle='--', alpha=0.7)

# Save and show plot
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_4")
image_name = 'f04020.pdf'
image_path = os.path.join(image_folder, image_name)
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()