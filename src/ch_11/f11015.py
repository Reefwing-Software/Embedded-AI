# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm

# Simulate a sine wave as the original analog signal
sample_count = 500
t = np.linspace(0, 1, sample_count)
analog_signal = 0.5 * np.sin(2 * np.pi * 5 * t) + 0.5  # Normalize to [0,1]

# Simulate PDM by oversampling and comparing to accumulator
pdm_signal = []
acc = 0.0
for val in analog_signal:
    for _ in range(8):  # Oversample to simulate high-rate PDM
        acc += val - 0.5
        if acc >= 0:
            pdm_signal.append(1)
            acc -= 1.0
        else:
            pdm_signal.append(0)

pdm_signal = np.array(pdm_signal)

# Simple PDM to PCM conversion using a moving average (low-pass filter)
kernel_size = 64
pcm_signal = np.convolve(pdm_signal, np.ones(kernel_size)/kernel_size, mode='valid')

# Resize time axis for plotting
pdm_time = np.linspace(0, 1, len(pdm_signal))
pcm_time = np.linspace(0, 1, len(pcm_signal))

# Set up custom font
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_11_final")
image_name = 'f11015.pdf'
image_path = os.path.join(image_folder, image_name)

# Plotting
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# PDM Plot
axes[0].plot(pdm_time, pdm_signal, color='black', linewidth=0.5)
axes[0].set_title("Simulated PDM signal", fontproperties=prop)
axes[0].set_xlabel("Time", fontproperties=prop)
axes[0].set_ylabel("Bit", fontproperties=prop)
axes[0].set_xlim(0.0, 0.1)  # Limit x-axis
axes[0].grid(True, which='both', linestyle='--', linewidth=0.5)

# PCM Plot
axes[1].plot(pcm_time, pcm_signal, color='black')
axes[1].set_title("Recovered PCM signal", fontproperties=prop)
axes[1].set_xlabel("Time", fontproperties=prop)
axes[1].set_ylabel("Amplitude", fontproperties=prop)
axes[1].set_xlim(0.0, 0.1)  # Limit x-axis
axes[1].grid(True, which='both', linestyle='--', linewidth=0.5)

plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()