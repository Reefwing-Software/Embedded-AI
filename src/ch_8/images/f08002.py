# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_8_v4")
image_name = 'f08002.pdf'
image_path = os.path.join(image_folder, image_name)

# Define parameters
frequencies = np.logspace(0, 6, 500)  # Frequencies from 1 Hz to 1,000,000 Hz
cutoff_frequency = 1000  # Cutoff frequency in Hz

# RC Low-Pass Filter Model
def low_pass_filter(f, fc):
    return 1 / np.sqrt(1 + (f / fc) ** 2)

# RC High-Pass Filter Model
def high_pass_filter(f, fc):
    return (f / fc) / np.sqrt(1 + (f / fc) ** 2)

# Calculate gain in dB
lowpass_gain = 20 * np.log10(low_pass_filter(frequencies, cutoff_frequency))
highpass_gain = 20 * np.log10(high_pass_filter(frequencies, cutoff_frequency))

# Create the plot
fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # Two charts side by side

# Left-hand chart: Low-pass filter
axes[0].plot(frequencies, lowpass_gain, color='black', label="Low-Pass Filter")
axes[0].axvline(x=cutoff_frequency, color='grey', linestyle='--', label="Cutoff frequency")
axes[0].fill_between(frequencies, lowpass_gain, -60, where=(frequencies < cutoff_frequency),
                     color='lightgrey', alpha=0.5, label="Passband")
axes[0].fill_between(frequencies, lowpass_gain, -60, where=(frequencies > cutoff_frequency),
                     color='darkgrey', alpha=0.5, label="Stopband")

# Chart settings for the left-hand plot
axes[0].set_xscale('log')
axes[0].set_xlabel("Frequency (Hz)", fontproperties=prop)
axes[0].set_ylabel("Gain (dB)", fontproperties=prop)
axes[0].set_title("Low-pass filter response", fontproperties=prop)
axes[0].set_ylim(-60, 5)
axes[0].set_xlim(1, 1e6)
axes[0].legend(prop=prop)
axes[0].grid(axis='y', linestyle='--', color='grey', alpha=0.7)  # Only y-axis gridlines

# Right-hand chart: High-pass filter
axes[1].plot(frequencies, highpass_gain, color='black', label="High-pass filter")
axes[1].axvline(x=cutoff_frequency, color='grey', linestyle='--', label="Cutoff frequency")
axes[1].fill_between(frequencies, -60, highpass_gain, where=(frequencies > cutoff_frequency),
                     color='lightgrey', alpha=0.5, label="Passband")
axes[1].fill_between(frequencies, -60, highpass_gain, where=(frequencies < cutoff_frequency),
                     color='darkgrey', alpha=0.5, label="Stopband")

# Chart settings for the right-hand plot
axes[1].set_xscale('log')
axes[1].set_xlabel("Frequency (Hz)", fontproperties=prop)
axes[1].set_ylabel("Gain (dB)", fontproperties=prop)
axes[1].set_title("High-pass filter response", fontproperties=prop)
axes[1].set_ylim(-60, 5)
axes[1].set_xlim(1, 1e6)
axes[1].legend(prop=prop)
axes[1].grid(axis='y', linestyle='--', color='grey', alpha=0.7)  # Only y-axis gridlines

# Add font properties to tick labels for both charts
for ax in axes:
    ax.tick_params(colors='black', labelsize=10)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(prop)

# Save and show the plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()