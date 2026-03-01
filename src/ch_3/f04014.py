# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import os

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_4")
image_name = 'f04014.pdf'
image_path = os.path.join(image_folder, image_name)

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
plt.plot(X, y, 'k.', markersize=10, label='Observations')
plt.plot(x, y_pred, 'k-', label='Prediction', linestyle='solid')
plt.fill_between(x.ravel(), y_pred - 1.96 * sigma, y_pred + 1.96 * sigma,
                 alpha=0.2, color='grey', label='95% confidence interval')

# Customizing the plot
plt.xlabel('Input', fontproperties=prop)
plt.ylabel('Output', fontproperties=prop)
# plt.title('Gaussian Process Regression', fontproperties=prop)
plt.legend(loc='upper left', prop=prop)
plt.grid(True, linestyle="--", linewidth=0.5)

# Save and show the plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()