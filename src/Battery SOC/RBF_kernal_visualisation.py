# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt

# Define the RBF kernel function
def rbf_kernel(x, x0, length_scale):
    return np.exp(-0.5 * ((x - x0) / length_scale)**2)

# Generate data for plotting
x = np.linspace(-5, 5, 400)
x0 = 0  # Center of the Gaussian curve
length_scale = 1.0  # Length scale parameter for the RBF kernel

# Calculate the RBF kernel values
y = rbf_kernel(x, x0, length_scale)

# Plot the RBF kernel function
plt.figure(figsize=(10, 6))
plt.plot(x, y, label=f'RBF Kernel (length_scale={length_scale})', color='blue')

# Annotate the plot
plt.axvline(x0, color='red', linestyle='--', label='Center Point (x0)')
plt.title('RBF Kernel Function Visualization')
plt.xlabel('Distance from Center (x - x0)')
plt.ylabel('Kernel Value')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()