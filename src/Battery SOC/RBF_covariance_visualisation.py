# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Define the RBF kernel function
def rbf_kernel(x1, x2, length_scale):
    return np.exp(-0.5 * (np.subtract.outer(x1, x2) / length_scale)**2)

# Generate sample data points
x = np.linspace(-5, 5, 10)

# Compute the covariance matrix using the RBF kernel
length_scale = 1.0
cov_matrix = rbf_kernel(x, x, length_scale)

# Plot the covariance matrix as a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(cov_matrix, annot=True, cmap='viridis', xticklabels=np.round(x, 2), yticklabels=np.round(x, 2))

# Annotate the plot
plt.title('Covariance Matrix Heatmap using RBF Kernel')
plt.xlabel('Data Points')
plt.ylabel('Data Points')

# Show the plot
plt.show()