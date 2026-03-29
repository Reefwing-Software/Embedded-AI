# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# Chapter 6: EDA - Effect of Low Pass Filter or Moving Average
# Figure 6-4

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)
# print(prop.get_name()) # Futura Std

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_5_v6")
image_name = 'f05002.pdf'
image_path = os.path.join(image_folder, image_name) 

# Generate a sample signal: a combination of a low-frequency and a high-frequency component
fs = 500  # Sampling frequency
t = np.arange(0, 1.0, 1.0/fs)  # Time vector
freq_low = 5  # Frequency of the low-frequency component
freq_high = 50  # Frequency of the high-frequency component

signal = np.sin(2 * np.pi * freq_low * t) + 0.5 * np.sin(2 * np.pi * freq_high * t)

# Apply a simple moving average filter (low-pass filter)
window_size = 20
filtered_signal = np.convolve(signal, np.ones(window_size)/window_size, mode='same')

# Plot the original and filtered signals
plt.figure(figsize=(14, 7))
plt.plot(t, signal, label='Original signal', color='lightgray')
plt.plot(t, filtered_signal, label='Filtered signal (low-pass)', color='black')
# plt.title('Low-pass Filter Effect')
plt.xlabel('Time [s]', fontproperties=prop)
plt.ylabel('Amplitude', fontproperties=prop)
plt.legend(prop=prop)
plt.grid()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()

