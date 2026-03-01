# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_8")
image_name = 'f08022.pdf'
image_path = os.path.join(image_folder, image_name)

# Generate the ideal circle data
theta = np.linspace(0, 2 * np.pi, 360)
radius = 0.5
Mx = radius * np.cos(theta)
My = radius * np.sin(theta)

# Add some random noise to simulate real sensor readings
noise_level = 0.01
Mx_noisy = Mx + np.random.normal(0, noise_level, Mx.shape)
My_noisy = My + np.random.normal(0, noise_level, My.shape)

# Create the scatter plot
plt.figure(figsize=(4, 4))
plt.scatter(Mx_noisy, My_noisy, color='grey', s=10)

# Draw the perfect circle for reference
circle = plt.Circle((0, 0), radius, color='black', fill=False, linestyle='--')
plt.gca().add_artist(circle)

# Draw black lines for the x and y axes
plt.axhline(0, color='black', linewidth=1.5)
plt.axvline(0, color='black', linewidth=1.5)

# Set axis limits and labels
plt.xlim(-0.7, 0.7)
plt.ylim(-0.7, 0.7)
plt.gca().set_aspect('equal', adjustable='box')

plt.xlabel('$M_x$ (G)', fontproperties=prop, color='black')
plt.ylabel('$M_y$ (G)', fontproperties=prop, color='black')

# Set the grid and background
plt.grid(True, color='grey', linestyle=':', linewidth=0.5)
plt.gca().set_facecolor('white')

# Show plot
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()