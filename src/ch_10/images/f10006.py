# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_10_v3")
image_name = 'f10006.pdf'
image_path = os.path.join(image_folder, image_name)

# Define levels
noise_floor = 30
nominal_level = 94
peak_level = 126
dynamic_range = peak_level - noise_floor
headroom = peak_level - nominal_level
snr = nominal_level - noise_floor

# Create plot
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_ylim(20, 143)
ax.set_xlim(0, 1)
ax.set_xticks([])

# Plot regions
ax.fill_between([0, 1], noise_floor, 130, color='lightgrey', label='Noise "floor"')
ax.fill_between([0, 1], peak_level, 143, color='darkgrey', label='Distortion region')

# Horizontal lines
ax.hlines([noise_floor, nominal_level, peak_level], 0, 1, colors='black', linestyles='dotted')

# Annotated labels
ax.text(0.5, peak_level + 1, 'Peak level\n(clipping point)', ha='center', va='bottom', fontproperties=prop)
ax.text(0.5, nominal_level + 1, 'Nominal level', ha='center', va='bottom', fontproperties=prop)
ax.text(0.75, noise_floor + 15, 'Noise "floor"\n(EIN: 30 dB SPL)', ha='center', va='top', fontproperties=prop)

# Arrows for SNR, Headroom, and Dynamic Range
ax.annotate('', xy=(0.4, nominal_level), xytext=(0.4, noise_floor),
            arrowprops=dict(arrowstyle='<->', color='black'))
ax.text(0.43, (nominal_level + noise_floor) / 2, f'SNR\n{snr} dB', fontproperties=prop, va='center')

ax.annotate('', xy=(0.8, peak_level), xytext=(0.8, nominal_level),
            arrowprops=dict(arrowstyle='<->', color='black'))
ax.text(0.83, (peak_level + nominal_level) / 2, f'Headroom\n{headroom} dB', fontproperties=prop, va='center')

ax.annotate('', xy=(0.05, peak_level), xytext=(0.05, noise_floor),
            arrowprops=dict(arrowstyle='<->', color='black'))
ax.text(0.08, (peak_level + noise_floor) / 2, f'Dynamic range\n{dynamic_range} dB', fontproperties=prop, va='center')

# Axis labels
ax.set_ylabel("Sound pressure level (dB SPL)", fontproperties=prop)
ax.set_title("T3902 microphone dynamic range", fontproperties=prop)

# Grid
ax.grid(True, axis='y', linestyle='--', linewidth=0.5, color='gray', alpha=0.6)

# Save and show
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()