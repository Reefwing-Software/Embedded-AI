# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

config = {
    'trial': 4,
    'initial_constant_value': 0.4,
    'constant_bounds': (0.1, 1.0),
    'initial_length_scales': [0.001, 0.5, 1.0],
    'length_scale_bounds': (0.001, 0.1),
    'max_iter': 20000,
    'n_restarts_optimizer': 10,
    'cv_folds': 5
}

# Create a pipeline with standardization and GPR
pipeline = Pipeline([
    ('gpr', gpr)
])