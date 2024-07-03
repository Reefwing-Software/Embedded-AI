# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib, os, time

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

# Define the GPR model with initial kernel
# Adjust bounds based on previous trials' results
kernel = C(0.1, (0.1, 1.0)) * RBF(0.5, (0.001, 0.1))
gpr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, optimizer='fmin_l_bfgs_b', max_iter=10000, random_state=42)

# Create a pipeline with standardization and GPR
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('gpr', gpr)
])

# Define the hyperparameter grid to optimize
param_grid = {
    'gpr__kernel': [
        C(0.1, (0.1, 1.0)) * RBF(0.5, (0.001, 0.1)),
        C(0.1, (0.1, 1.0)) * RBF(0.25, (0.001, 0.1)),
        C(0.1, (0.1, 1.0)) * RBF(1.0, (0.001, 0.1))
    ]
}

# Set up the grid search with cross-validation
grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=2)

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

# Load the best model (example of how to load it later)
# best_gpr_model = joblib.load(model_file)