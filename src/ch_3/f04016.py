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
image_name = 'f04016.pdf'
image_path = os.path.join(image_folder, image_name)

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
constant_value = 0.2  # Increased constant value for a more noticeable effect

# Compute the covariance matrix using the combined kernel
rbf_cov_matrix = rbf_kernel(x, x, length_scale)
constant_cov_matrix = constant_kernel(x, x, constant_value)
combined_cov_matrix = rbf_cov_matrix + constant_cov_matrix

# Plot the covariance matrix as a heatmap
plt.figure(figsize=(15, 6))

# Plot RBF Covariance Matrix
plt.subplot(1, 3, 1)
plt.imshow(rbf_cov_matrix, cmap='Greys', interpolation='nearest', vmin=0, vmax=rbf_cov_matrix.max() + constant_value)
plt.colorbar(label='Covariance value')
plt.xticks(ticks=np.arange(0, len(x), 2), labels=np.round(x[::2], 2), fontproperties=prop)
plt.yticks(ticks=np.arange(0, len(x), 2), labels=np.round(x[::2], 2), fontproperties=prop)
plt.grid(visible=True, linestyle='--', linewidth=0.5)
plt.title('RBF kernel covariance', fontproperties=prop)
plt.xlabel('Data points', fontproperties=prop)
plt.ylabel('Data points', fontproperties=prop)

# Plot Constant Covariance Matrix
plt.subplot(1, 3, 2)
plt.imshow(constant_cov_matrix, cmap='Greys', interpolation='nearest', vmin=0, vmax=rbf_cov_matrix.max() + constant_value)
plt.colorbar(label='Covariance value')
plt.xticks(ticks=np.arange(0, len(x), 2), labels=np.round(x[::2], 2), fontproperties=prop)
plt.yticks(ticks=np.arange(0, len(x), 2), labels=np.round(x[::2], 2), fontproperties=prop)
plt.grid(visible=True, linestyle='--', linewidth=0.5)
plt.title('Constant kernel covariance', fontproperties=prop)
plt.xlabel('Data points', fontproperties=prop)
plt.ylabel('Data points', fontproperties=prop)

# Plot Combined Covariance Matrix
plt.subplot(1, 3, 3)
plt.imshow(combined_cov_matrix, cmap='Greys', interpolation='nearest', vmin=0, vmax=rbf_cov_matrix.max() + constant_value)
plt.colorbar(label='Covariance value')
plt.xticks(ticks=np.arange(0, len(x), 2), labels=np.round(x[::2], 2), fontproperties=prop)
plt.yticks(ticks=np.arange(0, len(x), 2), labels=np.round(x[::2], 2), fontproperties=prop)
plt.grid(visible=True, linestyle='--', linewidth=0.5)
plt.title('Combined kernel covariance (RBF + constant)', fontproperties=prop)
plt.xlabel('Data points', fontproperties=prop)
plt.ylabel('Data points', fontproperties=prop)

# Save and show the plots
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()