# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import joblib
import numpy as np
from sklearn.utils.validation import check_array
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.gaussian_process.kernels import Kernel, Hyperparameter
from scipy.optimize import fmin_l_bfgs_b

# Define the hyperparameters in a configuration dictionary for Trial 6
config = {
    'trial': 6,
    'initial_constant_value': 0.079056,  # Squared value of 0.281
    'constant_bounds': (0.01, 1.0),  # Same bounds to allow exploration
    'initial_length_scales': [0.01, 0.05, 0.1],  # Avoiding very small initial values
    'length_scale_bounds': (0.01, 1.0),  # Adjusting bounds to avoid near-zero values
    'max_iter': 30000,  # Keeping high to allow thorough optimization
    'n_restarts_optimizer': 15,  # Same number of restarts for robustness
    'cv_folds': 5,  # Keeping the same cross-validation folds
    'standardize': True  # Continue standardizing the data
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

# Define file paths
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

# Feature names used during training
feature_names = ['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current']

# Load the saved model
gpr_model = joblib.load(model_file)

# Function to evaluate the model
def evaluate_model(model, X_test, Y_test):
    Y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(Y_test, Y_pred))
    mae = mean_absolute_error(Y_test, Y_pred)
    r2 = r2_score(Y_test, Y_pred)
    return rmse, mae, r2

# Test the model on each resampled test dataset
results = []

for test_label, test_file in test_files.items():
    test_path = os.path.join(preprocessed_folder, test_file)
    
    # Load the test data
    test_df = pd.read_csv(test_path)
    
    # Extract features and target
    X_test = test_df[feature_names]
    Y_test = test_df['SOC']
    
    # Evaluate the model
    try:
        rmse, mae, r2 = evaluate_model(gpr_model, X_test, Y_test)
        results.append({
            'Dataset': test_label,
            'RMSE': rmse,
            'MAE': mae,
            'R²': r2
        })
        print(f"Results for {test_label}: RMSE={rmse:.4f}, MAE={mae:.4f}, R²={r2:.4f}")
    except Exception as e:
        print(f"Error testing {test_label}: {e}")

# Print all results
print("\nPerformance Metrics for Resampled Test Data:")
for result in results:
    print(result)