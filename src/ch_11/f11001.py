# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm
from scipy.signal import butter, filtfilt

# Generate synthetic audio signal
fs = 1000  # Sampling frequency (Hz)
t = np.linspace(0, 1.0, int(fs), endpoint=False)  # 1 second of audio
signal = np.sin(2 * np.pi * 5 * t)  # 5 Hz sine wave (clean signal)

# Add high-frequency noise
noise = 0.5 * np.random.normal(size=t.shape)
noisy_signal = signal + noise

# Apply low-pass filter
def butter_lowpass_filter(data, cutoff, fs, order=4):
    nyq = 0.5 * fs  # Nyquist frequency
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

filtered_signal = butter_lowpass_filter(noisy_signal, cutoff=10, fs=fs)

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_11_final")
image_name = 'f11001.pdf'
image_path = os.path.join(image_folder, image_name)

# Plotting
plt.style.use('grayscale')
fig, axs = plt.subplots(1, 2, figsize=(10, 4))

axs[0].plot(t, noisy_signal, linewidth=1)
axs[0].set_title("Noisy signal", fontproperties=prop)
axs[0].set_xlabel("Time [s]", fontproperties=prop)
axs[0].set_ylabel("Amplitude", fontproperties=prop)
axs[0].grid(True)

axs[1].plot(t, filtered_signal, linewidth=1)
axs[1].set_title("Filtered signal", fontproperties=prop)
axs[1].set_xlabel("Time [s]", fontproperties=prop)
axs[1].set_ylabel("Amplitude", fontproperties=prop)
axs[1].grid(True)

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()