# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from scipy.signal import savgol_filter

# Set the random seed for reproducibility
np.random.seed(42)

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_10_final")
image_name = 'f10001.pdf'
image_path = os.path.join(image_folder, image_name)

# Create a synthetic ground truth signal
t = np.linspace(0, 10, 500)
true_signal = np.sin(t)

# Create non-Gaussian noise
noise = 0.2 * np.random.randn(len(t))
impulsive_noise = np.random.choice([0, 1], size=len(t), p=[0.98, 0.02]) * np.random.uniform(-2, 2, size=len(t))
noisy_measurement = true_signal + noise + impulsive_noise

# Simulate Kalman Filter
kalman_output = np.zeros_like(t)
P = 1.0
Q = 0.01
R = 0.1
x_hat = 0.0

for i in range(len(t)):
    P += Q
    K = P / (P + R)
    x_hat += K * (noisy_measurement[i] - x_hat)
    P *= (1 - K)
    kalman_output[i] = x_hat

# Simulate ML output
ml_output = savgol_filter(noisy_measurement, window_length=31, polyorder=3)

# Create the plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4), sharey=True)

# Full range plot
ax1.plot(t, true_signal, color='black', label='Ground truth', linewidth=1.5)
ax1.plot(t, noisy_measurement, color='0.7', label='Noisy measurement', linewidth=1)
ax1.plot(t, kalman_output, color='0.4', linestyle='--', label='Kalman filter output', linewidth=1.2)
ax1.plot(t, ml_output, color='0.2', linestyle='-.', label='ML model output', linewidth=1.2)
ax1.set_title("Full signal (0–10 s)", fontproperties=prop)
ax1.set_xlabel("Time (s)", fontproperties=prop)
ax1.set_ylabel("Signal", fontproperties=prop)
ax1.grid(True, linestyle='--', linewidth=0.5)
ax1.legend(prop=prop)

# Zoomed-in plot
ax2.plot(t, true_signal, color='black', linewidth=1.5)
ax2.plot(t, noisy_measurement, color='0.7', linewidth=1)
ax2.plot(t, kalman_output, color='0.4', linestyle='--', linewidth=1.2)
ax2.plot(t, ml_output, color='0.2', linestyle='-.', linewidth=1.2)
ax2.set_xlim(7, 9)
ax2.set_title("Zoomed-in (7–9 s)", fontproperties=prop)
ax2.set_xlabel("Time (s)", fontproperties=prop)
ax2.grid(True, linestyle='--', linewidth=0.5)

# Apply custom font to ticks
for ax in (ax1, ax2):
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontproperties(prop)

# Save and display
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()