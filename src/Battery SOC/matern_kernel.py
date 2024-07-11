# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from sklearn.gaussian_process.kernels import Kernel, Hyperparameter
from sklearn.utils.validation import check_array
from sklearn.gaussian_process.kernels import RBF, Matern, RationalQuadratic
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from scipy.optimize import fmin_l_bfgs_b
from sklearn.metrics import mean_squared_error, max_error

import numpy as np
import pandas as pd
import joblib, os, time
import matplotlib.pyplot as plt

# Define the hyperparameters in a configuration dictionary
config = {
    'trial': 8,
    'initial_constant_value': 0.079056,  # Squared value of 0.281
    'constant_bounds': (0.01, 1.0),  # Same bounds to allow exploration
    'initial_length_scales': [0.01, 0.05, 0.1],  # Avoiding very small initial values
    'length_scale_bounds': (0.01, 1.0),  # Adjusting bounds to avoid near-zero values
    'max_iter': 30000,  # Keeping high to allow thorough optimization
    'n_restarts_optimizer': 15,  # Same number of restarts for robustness
    'cv_folds': 5,  # Keeping the same cross-validation folds
    'standardize': True  # Continue standardizing the data
}

# Custom loss functions
def trimmed_rmse(y_true, y_pred):
    y_pred_trimmed = np.clip(y_pred, 0, 1)
    return np.sqrt(mean_squared_error(y_true, y_pred_trimmed))

def trimmed_max_abs_error(y_true, y_pred):
    y_pred_trimmed = np.clip(y_pred, 0, 1)
    return max_error(y_true, y_pred_trimmed)

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

# Load the training data
train_df = pd.read_csv(train_file)

# Extract features and target variable
X_train = train_df[['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current']]
y_train = train_df['SOC']

# Define the GPR model with a different kernel (e.g., Matern)
new_kernel = C(config['initial_constant_value'], config['constant_bounds']) * Matern(nu=2.5, length_scale=config['initial_length_scales'][0], length_scale_bounds=config['length_scale_bounds'])
gpr_new = GaussianProcessRegressor(kernel=new_kernel, optimizer=custom_optimizer, n_restarts_optimizer=config['n_restarts_optimizer'], random_state=42)

# Create a new pipeline
pipeline_new = Pipeline([
    ('scaler', StandardScaler() if config['standardize'] else 'passthrough'),
    ('gpr', gpr_new)
])

# Define the hyperparameter grid to optimize for the new kernel
param_grid_new = {
    'gpr__kernel': [
        C(config['initial_constant_value'], config['constant_bounds']) * Matern(nu=2.5, length_scale=length_scale, length_scale_bounds=config['length_scale_bounds'])
        for length_scale in config['initial_length_scales']
    ]
}

# Set up the grid search with cross-validation
grid_search_new = GridSearchCV(pipeline_new, param_grid_new, cv=config['cv_folds'], n_jobs=-1, verbose=2)

# Start the timer for the grid search
grid_search_start_time = time.time()

# Fit the model
grid_search_new.fit(X_train, y_train)

# Print the elapsed time for grid search
grid_search_elapsed_time = time.time() - grid_search_start_time
grid_search_minutes, grid_search_seconds = divmod(grid_search_elapsed_time, 60)
print(f"Grid search completed in {int(grid_search_minutes)} minutes and {grid_search_seconds:.2f} seconds")


# Output the best parameters and the corresponding score
print(f"Best parameters found: {grid_search_new.best_params_}")
print(f"Best cross-validation score: {grid_search_new.best_score_}")

# Print the actual parameter values of the best model
best_kernel_new = grid_search_new.best_estimator_.named_steps['gpr'].kernel_
print(f"Actual parameters of the best kernel: {best_kernel_new}")

# Save the best model
model_file = os.path.join(model_folder, 'best_matern_model.pkl')
joblib.dump(grid_search_new.best_estimator_, model_file)

# Print the total elapsed time for the script
total_elapsed_time = time.time() - start_time
total_minutes, total_seconds = divmod(total_elapsed_time, 60)
print(f"Total script execution time: {int(total_minutes)} minutes and {total_seconds:.2f} seconds")

# Print out the hyperparameters used in this trial
print("\nHyperparameters used in this trial:")
for key, value in config.items():
    print(f"{key}: {value}")

# Standardize the test data
scaler = StandardScaler()
X_test_scaled_list = [pd.DataFrame(scaler.transform(X), columns=X.columns) for X in X_test_list]

# Assign Best Model
best_model= grid_search_new.best_estimator_

# Calculate RMSE and Max Absolute Error for each temperature
rmse_list = []
max_abs_error_list = []

for X_test_scaled, y_test in zip(X_test_scaled_list, y_test_list):
    y_pred = best_model.predict(X_test_scaled)
    rmse_list.append(trimmed_rmse(y_test, y_pred))
    max_abs_error_list.append(trimmed_max_abs_error(y_test, y_pred))

# Plotting
temperatures = ["-10°C", "0°C", "10°C", "25°C"]

# Assuming y_test and y_pred are your true and predicted SOC values

residuals = [y_test - np.clip(best_model.predict(X_test_scaled), 0, 1) for X_test_scaled, y_test in zip(X_test_scaled_list, y_test_list)]

# Flatten the lists for plotting
residuals = np.concatenate(residuals)
y_test_all = np.concatenate(y_test_list)

plt.figure(figsize=(10, 6))
plt.scatter(y_test_all, residuals, alpha=0.5)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('True SOC')
plt.ylabel('Residual (True - Predicted)')
plt.title('Residual Plot')
plt.show()

# Calculate additional metrics
mae_list = [np.mean(np.abs(y_test - np.clip(best_model.predict(X_test_scaled), 0, 1))) for X_test_scaled, y_test in zip(X_test_scaled_list, y_test_list)]
median_abs_error_list = [np.median(np.abs(y_test - np.clip(best_model.predict(X_test_scaled), 0, 1))) for X_test_scaled, y_test in zip(X_test_scaled_list, y_test_list)]

print(f'Mean Absolute Error for each temperature: {mae_list}')
print(f'Median Absolute Error for each temperature: {median_abs_error_list}')

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.bar(temperatures, rmse_list, color='blue')
plt.title('RMSE for Each Ambient Temperature')
plt.xlabel('Ambient Temperature')
plt.ylabel('RMSE')

plt.subplot(1, 2, 2)
plt.bar(temperatures, max_abs_error_list, color='red')
plt.title('Max Absolute Error for Each Ambient Temperature')
plt.xlabel('Ambient Temperature')
plt.ylabel('Max Absolute Error')

plt.tight_layout()
plt.show()

# Load the best model (example of how to load it later)
# best_gpr_model = joblib.load(model_file)