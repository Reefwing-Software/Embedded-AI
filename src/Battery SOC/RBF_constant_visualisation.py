# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

# Define the RBF kernel function
def rbf_kernel(x1, x2, length_scale):
    return np.exp(-0.5 * (np.subtract.outer(x1, x2) / length_scale)**2)

# Define the Constant Kernel function
def constant_kernel(x1, x2, constant_value):
    return constant_value * np.ones_like(np.subtract.outer(x1, x2))

# Generate sample data points
x = np.linspace(-5, 5, 10)

# Parameters
length_scale = 1.0
constant_value = 0.5

# Compute the covariance matrix using the combined kernel
rbf_cov_matrix = rbf_kernel(x, x, length_scale)
constant_cov_matrix = constant_kernel(x, x, constant_value)
combined_cov_matrix = rbf_cov_matrix + constant_cov_matrix

# Plot the covariance matrix as a heatmap
plt.figure(figsize=(12, 10))

# Plot RBF Covariance Matrix
plt.subplot(1, 3, 1)
sns.heatmap(rbf_cov_matrix, annot=True, cmap='viridis', xticklabels=np.round(x, 2), yticklabels=np.round(x, 2))
plt.title('RBF Kernel Covariance')
plt.xlabel('Data Points')
plt.ylabel('Data Points')

# Plot Constant Covariance Matrix
plt.subplot(1, 3, 2)
sns.heatmap(constant_cov_matrix, annot=True, cmap='viridis', xticklabels=np.round(x, 2), yticklabels=np.round(x, 2))
plt.title('Constant Kernel Covariance')
plt.xlabel('Data Points')
plt.ylabel('Data Points')

# Plot Combined Covariance Matrix
plt.subplot(1, 3, 3)
sns.heatmap(combined_cov_matrix, annot=True, cmap='viridis', xticklabels=np.round(x, 2), yticklabels=np.round(x, 2))
plt.title('Combined Kernel Covariance')
plt.xlabel('Data Points')
plt.ylabel('Data Points')

# Show the plots
plt.tight_layout()
plt.show()