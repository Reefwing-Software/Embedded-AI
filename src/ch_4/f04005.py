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
image_name = 'f04005.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the linear model parameters
slope = 1.05
intercept = 1.35

# Assume we use the y-intercept (x = 0)
x_value = 0

# True prediction based on the actual model
true_prediction = slope * x_value + intercept

# Generate a range of predictions for this x value
predictions = np.linspace(0, 5, 100)  # Increase resolution to improve precision

# Calculate the Mean Squared Error for each prediction
mse_values = [(np.square(true_prediction - pred)).mean() for pred in predictions]

# Find the minimum MSE and its corresponding prediction
min_mse_index = np.argmin(np.round(mse_values, 10))  # Rounding to avoid floating-point artifacts
min_mse_value = mse_values[min_mse_index]
min_prediction = predictions[min_mse_index]

# Plotting the MSE vs Predictions
plt.figure(figsize=(10, 6))
plt.scatter(predictions, mse_values, label='MSE', color='black')

# Highlighting the minimum point
plt.axvline(x=min_prediction, color='grey', linestyle='--', label=f'Min MSE at 1.35')
plt.scatter([min_prediction], [min_mse_value], color='grey', zorder=5)

# Updating labels, title, and legend with font properties
plt.xlabel('Prediction', fontproperties=prop)
plt.ylabel('Mean squared error (MSE)', fontproperties=prop)
# plt.title('MSE vs Prediction for y-intercept (x = 0)', fontproperties=prop)
plt.legend(prop=prop)

# Adding grid
plt.grid(True, linestyle='--', linewidth=0.5)

# Save and show plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches="tight")
plt.show()

# Print the minimum MSE and corresponding prediction
print(f"Minimum MSE: {min_mse_value:.10f} at Prediction: {min_prediction:.2f}")