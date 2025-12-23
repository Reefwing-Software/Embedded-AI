# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

config = {
    'trial': 2,
    'initial_constant_value': 0.01,
    'constant_bounds': (0.001, 1.0),
    'initial_length_scales': [0.25, 0.5, 1.0],
    'length_scale_bounds': (0.001, 0.1),
    'max_iter': 15000,
    'n_restarts_optimizer': 10,
    'cv_folds': 5
}

# Define the GPR model with initial kernel - TRIAL 2
kernel = C(config['initial_constant_value'], config['constant_bounds']) * 
         RBF(config['initial_length_scales'][0], config['length_scale_bounds'])
gpr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, 
      random_state=42)

# Create a pipeline with standardization and GPR
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('gpr', gpr)
])

# Define the hyperparameter grid to optimize
param_grid = {
    'gpr__kernel': [
        C(config['initial_constant_value'], config['constant_bounds']) * 
          RBF(length_scale, config['length_scale_bounds'])
            for length_scale in config['initial_length_scales']
    ]
}
