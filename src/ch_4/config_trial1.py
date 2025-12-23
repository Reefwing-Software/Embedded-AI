# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# Define the hyperparameters in a configuration dictionary
config = {
    'trial': 1,
    'initial_constant_value': 0.01,
    'constant_bounds': (0.001, 0.1),
    'initial_length_scales': [0.5, 0.25, 1.0],
    'length_scale_bounds': (0.01, 1.0),
    'max_iter': 15000,
    'n_restarts_optimizer': 10,
    'cv_folds': 5
}
