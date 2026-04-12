# Copyright (c) 2026 David Such
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
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_7_v4")
image_name = 'f07007.pdf'
image_path = os.path.join(image_folder, image_name)

# Generate data
angles = np.linspace(-200, 200, 400)  # Angle of inclination in degrees
angles_rad = np.radians(angles)  # Convert angles to radians

# Accelerometer outputs (assuming g = 1 for simplicity)
accel_x = np.sin(angles_rad)
accel_y = np.cos(angles_rad)

# Plotting
plt.figure(figsize=(14, 7))

# Plot x-axis accelerometer output
plt.plot(angles, accel_x, label='Acceleration x-axis', color='darkgray', linestyle='-', linewidth=2)

# Plot y-axis accelerometer output
plt.plot(angles, accel_y, label='Acceleration y-axis', color='black', linestyle='--', linewidth=2)

# Set axis labels with custom font
plt.xlabel('Angle of inclination (alpha) [degrees]', fontproperties=prop, color='black')
plt.ylabel('Accelerometer output [g]', fontproperties=prop, color='black')

# Set axis ranges
plt.xlim(-200, 200)
plt.ylim(-1, 1)

# Show grid
plt.grid(True, color='gray', linestyle='--', linewidth=0.5)

# Show legend
plt.legend(prop=prop, frameon=False, labelcolor='darkgray')

# Customize tick labels
plt.xticks(fontproperties=prop, color='darkgray')
plt.yticks(fontproperties=prop, color='darkgray')

# Show plot and save it
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()