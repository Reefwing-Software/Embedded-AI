# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import os

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_8")
image_name = 'f08009.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the angle of inclination in degrees
alpha_degrees = np.linspace(-90, 90, 400)
# Convert degrees to radians for the sine function
alpha_radians = np.radians(alpha_degrees)

# Calculate Ax(g) = sin(alpha)
ax_g = np.sin(alpha_radians)

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(alpha_degrees, ax_g, color='black')  # Plot in black

# Set the labels with the custom font
plt.xlabel(r"$\alpha\ (degrees)$", fontsize=14, color='black', fontproperties=prop)
plt.ylabel(r"$A_x(g)$", fontsize=14, color='black', fontproperties=prop)

# Set grid and background to grayscale
plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
plt.gca().set_facecolor('lightgray')

# Set the color of the ticks and labels
plt.tick_params(axis='x', colors='black')
plt.tick_params(axis='y', colors='black')

# Set the font properties for ticks
plt.xticks(fontproperties=prop)
plt.yticks(fontproperties=prop)

# Show plot and save it
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()