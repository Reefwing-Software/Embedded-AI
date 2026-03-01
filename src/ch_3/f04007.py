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
image_name = 'f04007.pdf'
image_path = os.path.join(image_folder, image_name)

# Set the seed for reproducibility
np.random.seed(0)

# Generate 50 x values between 0 and 10
X = np.linspace(0, 10, 50)

# Generate the corresponding y values with Gaussian noise
true_slope = 1.05
true_intercept = 1.35
noise = np.random.normal(0, 1, X.shape)
Y = true_slope * X + true_intercept + noise

# Store the data points
data_points = np.column_stack((X, Y))

# Add a column of ones to X to account for the intercept term
X_b = np.c_[np.ones((X.shape[0], 1)), X]

# Calculate the normal equation parameters
beta = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(Y)

# Display the parameters
intercept, slope = beta
print(f"Intercept: {intercept}")
print(f"Slope: {slope}")

# Plot the data points
plt.figure(figsize=(10, 6))
plt.scatter(X, Y, color='black', label='Data points')

# Plot the line of best fit
Y_pred = slope * X + intercept
plt.plot(X, Y_pred, color='grey', label='Predictions')

# Update font properties
plt.xlabel('X', fontproperties=prop)
plt.ylabel('Y', fontproperties=prop)
# plt.title('Predictions and Data Points', fontproperties=prop)
plt.legend(prop=prop)
plt.grid(True)

# Save and show plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches="tight")
plt.show()