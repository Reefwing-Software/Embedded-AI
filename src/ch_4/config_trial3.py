# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

config = {
    'trial': 3,
    'initial_constant_value': 0.4,
    'constant_bounds': (0.1, 1.0),
    'initial_length_scales': [0.001, 0.5, 1.0],
    'length_scale_bounds': (0.001, 0.1),
    'max_iter': 20000,
    'n_restarts_optimizer': 10,
    'cv_folds': 5
}

# Custom optimizer function to include max_iter
def custom_optimizer(obj_func, initial_theta, bounds):
    result = fmin_l_bfgs_b(obj_func, initial_theta, bounds=bounds, maxiter=config['max_iter'])
    return result[0], result[1]

# Define the GPR model with initial kernel - TRIAL 2
kernel = C(config['initial_constant_value'], config['constant_bounds']) * 
         RBF(config['initial_length_scales'][0], config['length_scale_bounds'])
gpr = GaussianProcessRegressor(kernel=kernel, optimizer=custom_optimizer, n_restarts_optimizer=config['n_restarts_optimizer'], random_state=42)