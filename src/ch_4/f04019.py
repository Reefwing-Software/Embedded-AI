# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_4")
image_name = 'f04019.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the RBF kernel function
def rbf_kernel(x, y, length_scale=1.0):
    """Radial basis function (RBF) kernel"""
    sqdist = np.sum((x - y) ** 2)
    return np.exp(-0.5 * sqdist / length_scale ** 2)

# Define the Exponential kernel function
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
plt.plot(x, rbf_values, label='RBF kernel', color='black', linestyle='-')
plt.title('RBF kernel', fontproperties=prop)
plt.xlabel('Distance', fontproperties=prop)
plt.ylabel('Kernel value', fontproperties=prop)
plt.grid(True, linestyle='--', linewidth=0.5)
plt.legend(prop=prop)

# Exponential kernel plot
plt.subplot(1, 2, 2)
plt.plot(x, exp_values, label='Exponential kernel', color='grey', linestyle='--')
plt.title('Exponential kernel', fontproperties=prop)
plt.xlabel('Distance', fontproperties=prop)
plt.ylabel('Kernel value', fontproperties=prop)
plt.grid(True, linestyle='--', linewidth=0.5)
plt.legend(prop=prop)

# plt.suptitle('Comparison of RBF and Exponential Kernels', fontproperties=prop)
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()