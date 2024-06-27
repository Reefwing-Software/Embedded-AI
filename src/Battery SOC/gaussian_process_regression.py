# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

# Generate sample data
np.random.seed(1)
X = np.random.uniform(-3., 3., 20)[:, np.newaxis]
y = np.sin(X).ravel()
y += 0.5 * (0.5 - np.random.rand(y.shape[0]))  # Add noise to targets

# Define the kernel: constant kernel * RBF kernel
kernel = C(1.0, (1e-4, 1e1)) * RBF(1, (1e-4, 1e1))

# Create and fit the Gaussian Process model
gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, alpha=0.1)
gp.fit(X, y)

# Make predictions
x = np.atleast_2d(np.linspace(-5, 5, 1000)).T
y_pred, sigma = gp.predict(x, return_std=True)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(X, y, 'r.', markersize=10, label='Observations')
plt.plot(x, y_pred, 'b-', label='Prediction')
plt.fill_between(x.ravel(), y_pred - 1.96 * sigma, y_pred + 1.96 * sigma,
                 alpha=0.2, color='k', label='95% confidence interval')
plt.xlabel('Input')
plt.ylabel('Output')
plt.title('Gaussian Process Regression')
plt.legend(loc='upper left')
plt.show()