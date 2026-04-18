# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_8_v4")
image_name = 'f08005.pdf'
image_path = os.path.join(image_folder, image_name)

# Simulated true position (e.g., sinusoidal movement)
time = np.linspace(0, 10, 100)  # 100 time steps
true_position = np.sin(time)

# Noisy measurements
np.random.seed(0)
measurement_noise = np.random.normal(0, 0.3, size=time.shape)
measurements = true_position + measurement_noise

# Kalman filter implementation
n = len(time)
kalman_estimates = np.zeros(n)
kalman_uncertainty = np.zeros(n)
estimated_position = 0.0
uncertainty = 1.0
process_variance = 0.1
measurement_variance = 0.3 ** 2

for t in range(n):
    # Prediction step
    predicted_position = estimated_position
    predicted_uncertainty = uncertainty + process_variance

    # Update step
    kalman_gain = predicted_uncertainty / (predicted_uncertainty + measurement_variance)
    estimated_position = predicted_position + kalman_gain * (measurements[t] - predicted_position)
    uncertainty = (1 - kalman_gain) * predicted_uncertainty

    # Store results
    kalman_estimates[t] = estimated_position
    kalman_uncertainty[t] = uncertainty

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(time, true_position, label="True position", color="k", linewidth=2)  # Greyscale for True Position
plt.scatter(time, measurements, label="Noisy measurements", color="gray", s=10)  # Greyscale for Measurements
plt.plot(time, kalman_estimates, label="Kalman filter estimate", color="black", linestyle="--", linewidth=2)  # Dashed line for Estimate
plt.fill_between(time, kalman_estimates - np.sqrt(kalman_uncertainty),
                 kalman_estimates + np.sqrt(kalman_uncertainty), color="lightgray", alpha=0.5,
                 label="Kalman filter uncertainty")

# Add grid lines, title, and labels with the specified font properties
plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
plt.title("Effect of Kalman filter on noisy data", fontsize=14, fontproperties=prop)
plt.xlabel("Time", fontsize=12, fontproperties=prop)
plt.ylabel("Position", fontsize=12, fontproperties=prop)
plt.legend(prop=prop)
plt.tight_layout()

# Save the plot as a PDF
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()