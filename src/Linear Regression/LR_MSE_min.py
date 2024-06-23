# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt

# Define the linear model parameters
slope = 1.05
intercept = 1.35

# Assume we use the y-intercept (x = 0)
x_value = 0

# True prediction based on the actual model
true_prediction = slope * x_value + intercept

# Generate a range of predictions for this x value
predictions = np.linspace(0, 5, 100)

# Calculate the Mean Squared Error for each prediction
mse_values = [(np.square(true_prediction - pred)).mean() for pred in predictions]

# Plotting the MSE vs Predictions
plt.figure(figsize=(10, 6))
plt.scatter(predictions, mse_values, label='MSE', color='blue')

plt.xlabel('Prediction')
plt.ylabel('Mean Squared Error (MSE)')
plt.title('MSE vs Prediction for y-intercept (x = 0)')
plt.legend()
plt.grid(True)
plt.show()