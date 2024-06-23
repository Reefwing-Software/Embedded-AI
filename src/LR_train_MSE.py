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

# Add a column of ones to X to account for the intercept term
X_b = np.c_[np.ones((X.shape[0], 1)), X]

# Calculate the normal equation parameters
beta = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(Y)

# Display the parameters
intercept, slope = beta
print(f"Intercept: {intercept}")
print(f"Slope: {slope}")

# Calculate the predicted Y values
Y_pred = X_b.dot(beta)

# Calculate the Mean Squared Error
mse = np.mean((Y - Y_pred) ** 2)
print(f"Mean Squared Error: {mse}")

# Plot the data points
plt.figure(figsize=(10, 6))
plt.scatter(X, Y, color='blue', label='Data Points')

# Plot the line of best fit
plt.plot(X, Y_pred, color='red', label='Line of Best Fit')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Line of Best Fit and Data Points')
plt.legend()
plt.grid(True)
plt.show()