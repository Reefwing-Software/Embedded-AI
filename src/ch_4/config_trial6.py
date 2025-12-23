# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

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
