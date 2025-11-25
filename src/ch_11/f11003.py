# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm
from scipy.signal import spectrogram

# Signal parameters
fs = 1000  # Sampling frequency
duration = 2.0  # seconds
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Stationary noise: white noise
stationary_noise = 0.5 * np.random.normal(size=t.shape)

# Non-stationary noise: bursts of white noise + silence
non_stationary_noise = np.zeros_like(t)
burst_times = np.arange(0.2, 1.8, 0.4)
for bt in burst_times:
    idx = (t >= bt) & (t < bt + 0.1)
    non_stationary_noise[idx] = 0.8 * np.random.normal(size=np.sum(idx))

# Font and image settings
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_11_final")
image_name = 'f11003.pdf'
image_path = os.path.join(image_folder, image_name)

# Plotting
plt.style.use('grayscale')
fig, axs = plt.subplots(1, 2, figsize=(12, 4))

# Spectrogram for stationary noise
f1, t1, Sxx1 = spectrogram(stationary_noise, fs)
axs[0].pcolormesh(t1, f1, 10 * np.log10(Sxx1 + 1e-10), shading='gouraud')
axs[0].set_title("Stationary noise", fontproperties=prop)
axs[0].set_xlabel("Time [s]", fontproperties=prop)
axs[0].set_ylabel("Frequency [Hz]", fontproperties=prop)

# Spectrogram for non-stationary noise
f2, t2, Sxx2 = spectrogram(non_stationary_noise, fs)
axs[1].pcolormesh(t2, f2, 10 * np.log10(Sxx2 + 1e-10), shading='gouraud')
axs[1].set_title("Non-stationary noise", fontproperties=prop)
axs[1].set_xlabel("Time [s]", fontproperties=prop)
axs[1].set_ylabel("Frequency [Hz]", fontproperties=prop)

# Layout and export
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()