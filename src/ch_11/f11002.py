# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm

# Time settings
fs = 1000  # Sampling frequency
t = np.linspace(0, 1.0, int(fs), endpoint=False)

# Desired signal: simulate a voice tone at 150 Hz
voice = 0.5 * np.sin(2 * np.pi * 150 * t)

# Background noise: 50 Hz hum + random noise
noise = 0.6 * np.sin(2 * np.pi * 50 * t) + 0.2 * np.random.normal(size=t.shape)

# Combined signal (what a mic would hear)
input_signal = voice + noise

# Anti-noise: estimate and invert only the 50 Hz component (not perfect)
estimated_noise = 0.6 * np.sin(2 * np.pi * 50 * t + np.pi * 0.95)  # slightly off-phase
anti_noise = -estimated_noise

# ANC output = input + anti-noise
anc_output = input_signal + anti_noise

# Font and image settings
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_11_final")
image_name = 'f11002.pdf'
image_path = os.path.join(image_folder, image_name)

# Plotting
plt.style.use('grayscale')
fig, axs = plt.subplots(1, 3, figsize=(14, 4))

axs[0].plot(t, input_signal, linewidth=1)
axs[0].set_title("Input signal (voice + noise)", fontproperties=prop)
axs[0].set_xlabel("Time [s]", fontproperties=prop)
axs[0].set_ylabel("Amplitude", fontproperties=prop)
axs[0].grid(True)

axs[1].plot(t, anti_noise, linewidth=1)
axs[1].set_title("Anti-noise signal", fontproperties=prop)
axs[1].set_xlabel("Time [s]", fontproperties=prop)
axs[1].set_ylabel("Amplitude", fontproperties=prop)
axs[1].grid(True)

axs[2].plot(t, anc_output, linewidth=1)
axs[2].set_title("ANC output (noise reduced)", fontproperties=prop)
axs[2].set_xlabel("Time [s]", fontproperties=prop)
axs[2].set_ylabel("Amplitude", fontproperties=prop)
axs[2].grid(True)

plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()