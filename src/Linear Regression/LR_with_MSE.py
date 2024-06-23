# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt

# Example data
X = np.array([1, 2, 3, 4, 5])
Y = np.array([2, 4, 5, 4.5, 7])

# Calculate the line of best fit using numpy's polyfit
coefficients = np.polyfit(X, Y, 1)
poly = np.poly1d(coefficients)

# Extract the coefficients
b1 = coefficients[0]  # Slope
b0 = coefficients[1]  # Intercept

# Generate the fitted values
Y_fit = poly(X)

# Calculate MSE
mse = np.mean((Y - Y_fit) ** 2)

# Plot the data points
plt.scatter(X, Y, color='blue', label='Data Points')

# Plot the line of best fit
plt.plot(X, Y_fit, color='red', linestyle='--', label=f'Line of Best Fit\n$y = {b1:.2f}x + {b0:.2f}$')

# Plot dotted lines for errors
for i in range(len(X)):
    plt.plot([X[i], X[i]], [Y[i], Y_fit[i]], 'k--', lw=0.8)

# Adding labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Linear Regression with MSE')
plt.legend()

# Display the MSE on the plot
plt.text(1, 5.5, f'Mean Squared Error (MSE): {mse:.2f}', fontsize=12, color='black')

# Show the plot
plt.show()

# Print the coefficients to verify
print(f"Intercept (b0): {b0}")
print(f"Slope (b1): {b1}")
print(f"Mean Squared Error (MSE): {mse:.2f}")
