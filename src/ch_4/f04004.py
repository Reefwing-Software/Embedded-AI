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
image_name = 'f04004.pdf'
image_path = os.path.join(image_folder, image_name)

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
plt.scatter(X, Y, color='black', label='Data points')

# Plot the line of best fit
plt.plot(X, Y_fit, color='grey', linestyle='--', label=f'Line of best fit\n$y = {b1:.2f}x + {b0:.2f}$', linewidth=1.5)

# Plot dotted lines for errors
for i in range(len(X)):
    plt.plot([X[i], X[i]], [Y[i], Y_fit[i]], 'k--', lw=0.8)

# Adding labels and title
plt.xlabel('X', fontproperties=prop)
plt.ylabel('Y', fontproperties=prop)
# plt.title('Linear Regression with MSE', fontproperties=prop)
plt.legend(prop=prop)

# Display the MSE on the plot
plt.text(1, 5.5, f'Mean squared error (MSE): {mse:.2f}', fontsize=12, fontproperties=prop, color='black')

# Save and show plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches="tight")
plt.show()

# Print the coefficients to verify
print(f"Intercept (b0): {b0}")
print(f"Slope (b1): {b1}")
print(f"Mean Squared Error (MSE): {mse:.2f}")