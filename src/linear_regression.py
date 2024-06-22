# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import matplotlib.pyplot as plt
import numpy as np

# Example data
X = np.array([1, 2, 3, 4, 5])
Y = np.array([2, 4, 5, 4.5, 7])

# Calculate the line of best fit
coefficients = np.polyfit(X, Y, 1)
poly = np.poly1d(coefficients)
line_of_best_fit = poly(X)

# Extract the coefficients
b1 = coefficients[0]  # Slope
b0 = coefficients[1]  # Intercept

# Plotting the data points
plt.scatter(X, Y, color='blue', label='Data Points')

# Plotting the line of best fit
plt.plot(X, line_of_best_fit, color='red', linestyle='--', label='Line of Best Fit')

# Adding labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Linear Regression')
plt.legend()

# Set the y-axis to start at 0
X_fit = np.linspace(X.min(), X.max(), 100)
Y_fit = poly(X_fit)
plt.xlim(0, max(X_fit.max(), X_fit.max()) + 1)
plt.ylim(0, max(Y_fit.max(), Y_fit.max()) + 1)

# Annotating the coefficients on the plot
plt.text(0.5, 0.25, f'Intercept (b0): {b0:.2f}\nSlope (b1): {b1:.2f}', 
         fontsize=12, color='green', transform=plt.gca().transAxes)

# Change the window title
fig = plt.gcf()
fig.canvas.manager.set_window_title('Figure 3')

# Display the plot
plt.show()