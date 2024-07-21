# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt

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
plt.plot(t, signal, label='Original Signal', color='orange')
plt.plot(t, filtered_signal, label='Filtered Signal (Low-pass)', color='blue')
plt.title('Low-pass Filter Effect')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.grid()
plt.show()