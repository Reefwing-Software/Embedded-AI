# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from sklearn.gaussian_process.kernels import Kernel
from sklearn.utils.validation import check_array
import numpy as np

class ExponentialKernel(Kernel):
    def __init__(self, length_scale=1.0):
        self.length_scale = length_scale

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

    @property
    def hyperparameter_length_scale(self):
        return Kernel.hyperparameter_length_scale

# Example usage in GPR
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from scipy.optimize import fmin_l_bfgs_b
import joblib
import os
import time

# Set the random seed for reproducibility
np.random.seed(42)

# Define the hyperparameters in a configuration dictionary for Trial 6
config = {
    'trial': 6,
    'initial_constant_value': 0.423401,  # Based on actual optimized value from Trial 3
    'constant_bounds': (0.1, 1.0),
    'initial_length_scales': [0.0001, 0.0002, 0.0005],
    'length_scale_bounds': (0.0001, 0.01),  # Expanded lower bound
    'max_iter': 20000,
    'n_restarts_optimizer': 10,
    'cv_folds': 5,
    'standardize': False
}

# Custom optimizer function to include max_iter
def custom_optimizer(obj_func, initial_theta, bounds):
    result = fmin_l_bfgs_b(obj_func, initial_theta, bounds=bounds, maxiter=config['max_iter'])
    return result[0], result[1]

# Start the timer for the complete script
start_time = time.time()

# Define the file paths
preprocessed_folder = os.path.expanduser("~/Documents/GitHub/Embedded-AI/data/LGHG2@n10C_to_25degC/Preprocessed")
model_folder = os.path.expanduser("~/Documents/GitHub/Embedded-AI/data/LGHG2@n10C_to_25degC/Model")
os.makedirs(model_folder, exist_ok=True)

# Define the training data file path (preprocessed)
train_file = os.path.join(preprocessed_folder, 'resampled_training_data.csv')

# Load the training data
train_df = pd.read_csv(train_file)

# Extract features and target variable
X_train = train_df[['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current']]
y_train = train_df['SOC']

# Define the GPR model with initial kernel for Trial 4
kernel = C(config['initial_constant_value'], config['constant_bounds']) * ExponentialKernel(config['initial_length_scales'][0])
gpr = GaussianProcessRegressor(kernel=kernel, optimizer=custom_optimizer, n_restarts_optimizer=config['n_restarts_optimizer'], random_state=42)

# Create a pipeline with standardization and GPR
pipeline = Pipeline([
    ('scaler', StandardScaler()),  # Reintroduce StandardScaler
    ('gpr', gpr)
])

# Define the hyperparameter grid to optimize
param_grid_trial_6 = {
    'gpr__kernel': [
        C(config['initial_constant_value'], config['constant_bounds']) * ExponentialKernel(length_scale)
        for length_scale in config['initial_length_scales']
    ]
}

# Set up the grid search with cross-validation
grid_search = GridSearchCV(pipeline, param_grid_trial_6, cv=config['cv_folds'], n_jobs=-1, verbose=2)

# Start the timer for the grid search
grid_search_start_time = time.time()

# Fit the model
grid_search.fit(X_train, y_train)

# Print the elapsed time for grid search
grid_search_elapsed_time = time.time() - grid_search_start_time
grid_search_minutes, grid_search_seconds = divmod(grid_search_elapsed_time, 60)
print(f"Grid search completed in {int(grid_search_minutes)} minutes and {grid_search_seconds:.2f} seconds")

# Output the best parameters and the corresponding score
print(f"Best parameters found: {grid_search.best_params_}")
print(f"Best cross-validation score: {grid_search.best_score_}")

# Print the actual parameter values of the best model
best_kernel = grid_search.best_estimator_.named_steps['gpr'].kernel_
print(f"Actual parameters of the best kernel: {best_kernel}")

# Save the best model
model_file = os.path.join(model_folder, 'best_gpr_model.pkl')
joblib.dump(grid_search.best_estimator_, model_file)

# Print the total elapsed time for the script
total_elapsed_time = time.time() - start_time
total_minutes, total_seconds = divmod(total_elapsed_time, 60)
print(f"Total script execution time: {int(total_minutes)} minutes and {total_seconds:.2f} seconds")

# Print out the hyperparameters used in this trial
print("\nHyperparameters used in this trial:")
for key, value in config.items():
    print(f"{key}: {value}")

# Load the best model (example of how to load it later)
# best_gpr_model = joblib.load(model_file)