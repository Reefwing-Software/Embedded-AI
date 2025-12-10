# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_12_final")
image_name = 'f12019.pdf'
image_path = os.path.join(image_folder, image_name)

# Define time intervals
time_steps = np.arange(0, 10, 1)

# Define MIDI note values for an ascending C Major arpeggio (C3, E3, G3, C4)
major_arpeggio = [48, 52, 55, 60, 48, 52, 55, 60, 48, 52]  # C, E, G, C

# Define MIDI note values for a descending C Augmented arpeggio (C4, E4, G#4, C3)
augmented_arpeggio = [72, 76, 80, 60, 72, 76, 80, 60, 72, 76]  # C, E, G#

# Create the figure and axes
fig, axes = plt.subplots(1, 2, figsize=(10, 5), dpi=300)

# Plot the ascending major arpeggio
axes[0].plot(time_steps, major_arpeggio, marker='o', linestyle='-', color='black')
axes[0].set_title("Ascending major arpeggio", fontproperties=prop)
axes[0].set_xlabel("Time", fontproperties=prop)
axes[0].set_ylabel("MIDI note", fontproperties=prop)
axes[0].grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Plot the descending augmented arpeggio
axes[1].plot(time_steps, augmented_arpeggio, marker='o', linestyle='-', color='black')
axes[1].set_title("Descending augmented arpeggio", fontproperties=prop)
axes[1].set_xlabel("Time", fontproperties=prop)
axes[1].set_ylabel("MIDI note", fontproperties=prop)
axes[1].grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Set the figure to greyscale
plt.style.use('grayscale')

# Show the plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()