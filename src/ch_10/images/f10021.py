# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# Generate time domain signal: sum of sine waves
fs = 1000  # Sampling frequency (Hz)
t = np.linspace(0, 1, fs, endpoint=False)
frequencies = [50, 120, 300]
signal = sum(np.sin(2 * np.pi * f * t) for f in frequencies)

# FFT
fft_vals = np.fft.fft(signal)
fft_freqs = np.fft.fftfreq(len(signal), 1/fs)
positive_freqs = fft_freqs[:fs // 2]
magnitude = np.abs(fft_vals)[:fs // 2]

# Font setup (update path as needed)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Image save path
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_10_v3")
os.makedirs(image_folder, exist_ok=True)
image_name = 'f10021.pdf'
image_path = os.path.join(image_folder, image_name)

# Plotting
fig, axs = plt.subplots(1, 2, figsize=(12, 4))

# Time domain
axs[0].plot(t, signal, color='black')
axs[0].set_title("Time domain", fontproperties=prop)
axs[0].set_xlabel("Time (s)", fontproperties=prop)
axs[0].set_ylabel("Amplitude", fontproperties=prop)
axs[0].grid(True)

# Frequency domain
axs[1].plot(positive_freqs, magnitude, color='black')
axs[1].set_title("Frequency domain (FFT)", fontproperties=prop)
axs[1].set_xlabel("Frequency (Hz)", fontproperties=prop)
axs[1].set_ylabel("Magnitude", fontproperties=prop)
axs[1].grid(True)

plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()