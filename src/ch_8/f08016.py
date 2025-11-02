# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import os

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_8")
image_name = 'f08016.pdf'
image_path = os.path.join(image_folder, image_name)

# Generate data
tilt_degrees = np.linspace(0, 90, 10)
tilt_radians = np.radians(tilt_degrees)

# Sensitivity simulation (in mg/degree)
sensitivity_arcsin = 17.5 * np.cos(tilt_radians)  # Reverse the Arcsin shape
sensitivity_arccos = 17.5 * np.sin(tilt_radians)  # Reverse the Arccos shape
sensitivity_arctan = 17.5 * np.ones_like(tilt_radians)  # Straight line approximation for Arctan(Ax/Az)

# Create the plot
plt.figure(figsize=(10, 6))

# Plotting the lines
plt.plot(tilt_degrees, sensitivity_arcsin, label='Arcsin(Ax)', color='black', linestyle='-')
plt.plot(tilt_degrees, sensitivity_arccos, label='Arccos(Az)', color='gray', linestyle='--')
plt.plot(tilt_degrees, sensitivity_arctan, label='Arctan(Ax/Az)', color='dimgray', linestyle='-.')

# Set the labels with the custom font
plt.xlabel('Tilt (degrees)', fontsize=14, color='black', fontproperties=prop)
plt.ylabel('Sensitivity (mg/degree)', fontsize=14, color='black', fontproperties=prop)

# Set grid and background to grayscale
plt.grid(True, color='lightgray', linestyle='--', linewidth=0.5)
plt.gca().set_facecolor('white')

# Set the y-axis range
plt.ylim(0, 20)

# Set the font properties for ticks
plt.xticks(fontproperties=prop)
plt.yticks(fontproperties=prop)

# Add a legend
plt.legend(prop=prop)

# Show plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()