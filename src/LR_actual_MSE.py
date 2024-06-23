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
theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(Y)

# Display the parameters from the normal equation
intercept, slope = theta_best
print(f"Calculated Intercept: {intercept}")
print(f"Calculated Slope: {slope}")

# Calculate the predicted Y values using the calculated parameters
Y_pred = X_b.dot(theta_best)

# Calculate the Mean Squared Error using the calculated parameters
mse_calculated = np.mean((Y - Y_pred) ** 2)
print(f"Mean Squared Error (Calculated Parameters): {mse_calculated}")

# Calculate the predicted Y values using the actual parameters
Y_actual_pred = true_slope * X + true_intercept

# Calculate the Mean Squared Error using the actual parameters
mse_actual = np.mean((Y - Y_actual_pred) ** 2)
print(f"Mean Squared Error (Actual Parameters): {mse_actual}")

# Plot the data points and the lines of best fit
plt.figure(figsize=(10, 6))
plt.scatter(X, Y, color='blue', label='Data Points')

# Plot the line of best fit using calculated parameters
plt.plot(X, Y_pred, color='red', label='Line of Best Fit (Calculated Parameters)')

# Plot the line of best fit using actual parameters
plt.plot(X, Y_actual_pred, color='green', linestyle='--', label='Line of Best Fit (Actual Parameters)')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Line of Best Fit and Data Points')
plt.legend()
plt.grid(True)
plt.show()