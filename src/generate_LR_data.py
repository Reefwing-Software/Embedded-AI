# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt

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

# Plot the data points
plt.scatter(X, Y, color='blue', label='Data Points with Noise')

# Adding labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Generated Data')
plt.legend()

# Display the plot
plt.show()

# Print the first few data points to verify
print("First 5 data points (X, Y):")
print(data_points[:5])
