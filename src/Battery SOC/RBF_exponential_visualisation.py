# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt

def rbf_kernel(x, y, length_scale=1.0):
    """Radial Basis Function (RBF) kernel"""
    sqdist = np.sum((x - y) ** 2)
    return np.exp(-0.5 * sqdist / length_scale ** 2)

def exponential_kernel(x, y, length_scale=1.0):
    """Exponential kernel"""
    dist = np.sqrt(np.sum((x - y) ** 2))
    return np.exp(-dist / length_scale)

# Generate a range of distances
x = np.linspace(-5, 5, 100).reshape(-1, 1)
y = np.zeros_like(x)

# Compute kernel values
rbf_values = np.array([rbf_kernel(xi, y[0]) for xi in x])
exp_values = np.array([exponential_kernel(xi, y[0]) for xi in x])

# Plot the kernels
plt.figure(figsize=(12, 6))

# RBF kernel plot
plt.subplot(1, 2, 1)
plt.plot(x, rbf_values, label='RBF Kernel', color='blue')
plt.title('RBF Kernel')
plt.xlabel('Distance')
plt.ylabel('Kernel Value')
plt.grid(True)
plt.legend()

# Exponential kernel plot
plt.subplot(1, 2, 2)
plt.plot(x, exp_values, label='Exponential Kernel', color='red')
plt.title('Exponential Kernel')
plt.xlabel('Distance')
plt.ylabel('Kernel Value')
plt.grid(True)
plt.legend()

plt.suptitle('Comparison of RBF and Exponential Kernels')
plt.show()