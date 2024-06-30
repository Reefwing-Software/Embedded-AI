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
import joblib, os

# Set the random seed for reproducibility
np.random.seed(42)

# Define the file paths
preprocessed_folder = os.path.expanduser("~/Documents/GitHub/Embedded-AI/data/LGHG2@n10C_to_25degC/preprocessed")
train_file = os.path.join(preprocessed_folder, 'resampled_training_data.csv')

# Load the training data
train_df = pd.read_csv(train_file)

# Extract features and target variable
X_train = train_df[['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current']]
y_train = train_df['SOC']

# Define the GPR model with initial kernel
kernel = C(1.0, (1e-2, 1e2)) * RBF(1.0, (1e-2, 1e2))
gpr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, random_state=42)

# Create a pipeline with standardization and GPR
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('gpr', gpr)
])

# Define the hyperparameter grid to optimize
param_grid = {
    'gpr__kernel': [
        C(1.0, (1e-2, 1e2)) * RBF(1.0, (1e-2, 1e2)),
        C(1.0, (1e-2, 1e2)) * RBF(0.5, (1e-2, 1e2)),
        C(1.0, (1e-2, 1e2)) * RBF(2.0, (1e-2, 1e2))
    ]
}

# Set up the grid search with cross-validation
grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=2)

# Fit the model
grid_search.fit(X_train, y_train)

# Output the best parameters and the corresponding score
print(f"Best parameters found: {grid_search.best_params_}")
print(f"Best cross-validation score: {grid_search.best_score_}")

# Save the best model
joblib.dump(grid_search.best_estimator_, 'best_gpr_model.pkl')

# Load the best model (example of how to load it later)
# best_gpr_model = joblib.load('best_gpr_model.pkl')