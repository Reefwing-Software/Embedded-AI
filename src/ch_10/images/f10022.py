# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# Create a simple signal (single sine wave)
fs = 1000  # Sampling frequency
t = np.linspace(0, 1, fs, endpoint=False)
frequency = 5  # Hz
signal = np.sin(2 * np.pi * frequency * t)

# Define a window (Hanning window)
window = np.hanning(len(signal))

# Apply the window
windowed_signal = signal * window

# Font and path setup
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_10_v3")
os.makedirs(image_folder, exist_ok=True)
image_name = 'f10022.pdf'
image_path = os.path.join(image_folder, image_name)

# Plotting
fig, axs = plt.subplots(1, 2, figsize=(12, 4))  # <-- side by side

# Original signal
axs[0].plot(t, signal, color='black', label='Original signal')
axs[0].set_title('Original signal without windowing', fontproperties=prop)
axs[0].set_xlabel('Time (s)', fontproperties=prop)
axs[0].set_ylabel('Amplitude', fontproperties=prop)
axs[0].grid(True)
axs[0].legend(prop=prop)

# Windowed signal
axs[1].plot(t, windowed_signal, color='black', label='Windowed signal')
axs[1].set_title('Signal after applying Hanning window', fontproperties=prop)
axs[1].set_xlabel('Time (s)', fontproperties=prop)
axs[1].set_ylabel('Amplitude', fontproperties=prop)
axs[1].grid(True)
axs[1].legend(prop=prop)

# Finalize and save
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()