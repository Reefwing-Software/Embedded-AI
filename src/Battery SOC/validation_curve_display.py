# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import validation_curve
from sklearn.metrics import make_scorer, r2_score
import matplotlib.pyplot as plt
import joblib
import os

# Import the custom kernel and optimizer
from custom_kernels import ExponentialKernel, custom_optimizer

# Define file paths
preprocessed_folder = os.path.expanduser("~/Documents/GitHub/Embedded-AI/data/LGHG2@n10C_to_25degC/Preprocessed")
model_folder = os.path.expanduser("~/Documents/GitHub/Embedded-AI/data/LGHG2@n10C_to_25degC/Model")
train_file = os.path.join(preprocessed_folder, 'resampled_training_data.csv')
model_file = os.path.join(model_folder, 'best_gpr_model.pkl')

# Load the training data
train_df = pd.read_csv(train_file)

# Extract features and target variable
X_train = train_df[['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current']]
y_train = train_df['SOC']

# Standardize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Load the saved model
best_gpr_model = joblib.load(model_file)

# Define the parameter range for the length scale
param_range = np.logspace(-3, 0, 10)

# Calculate the validation curve
train_scores, test_scores = validation_curve(
    best_gpr_model, X_train_scaled, y_train, 
    param_name="gpr__kernel__k2__length_scale",
    param_range=param_range, 
    cv=5, 
    scoring=make_scorer(r2_score)
)

# Compute mean and standard deviation of training and validation scores
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)

# Plot the validation curve
plt.figure()
plt.title("Validation Curve with GPR (Exponential Kernel)")
plt.xlabel("Length Scale")
plt.ylabel("Score (R^2)")
plt.ylim(0.0, 1.1)
plt.semilogx(param_range, train_scores_mean, label="Training score", color="darkorange", lw=2)
plt.fill_between(param_range, train_scores_mean - train_scores_std,
                 train_scores_mean + train_scores_std, alpha=0.2,
                 color="darkorange", lw=2)
plt.semilogx(param_range, test_scores_mean, label="Cross-validation score",
             color="navy", lw=2)
plt.fill_between(param_range, test_scores_mean - test_scores_std,
                 test_scores_mean + test_scores_std, alpha=0.2,
                 color="navy", lw=2)
plt.legend(loc="best")
plt.show()