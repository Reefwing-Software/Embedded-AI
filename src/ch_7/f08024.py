# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from matplotlib import font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_8")
image_name = 'f08024.pdf'
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

# Add soft iron distortion by scaling the axes differently
scale_x = 1.2  # Stretching factor for Mx (elliptical deformation)
scale_y = 0.8  # Compression factor for My
Mx_noisy = Mx_noisy * scale_x
My_noisy = My_noisy * scale_y

# Apply the same tilt to the data
rotation_angle = 20  # Degrees
rotation_radians = np.deg2rad(rotation_angle)

# Rotation matrix
rotation_matrix = np.array([[np.cos(rotation_radians), -np.sin(rotation_radians)],
                            [np.sin(rotation_radians),  np.cos(rotation_radians)]])

# Rotate the data
Mx_rotated, My_rotated = np.dot(rotation_matrix, np.array([Mx_noisy, My_noisy]))

# Add hard iron distortion by offsetting the data
offset_x = 0.2
offset_y = 0.2
Mx_rotated += offset_x
My_rotated += offset_y

# Create the scatter plot
plt.figure(figsize=(4, 4))
plt.scatter(Mx_rotated, My_rotated, color='grey', s=10)

# Draw the distorted circle with a tilt for reference
ax = plt.gca()

# Create the transformation: scale, rotate, and translate
ellipse_transform = (transforms.Affine2D()
                     .scale(scale_x, scale_y)
                     .rotate_deg(rotation_angle)
                     .translate(offset_x, offset_y)
                     + ax.transData)

# Create the ellipse with the transformation
ellipse = plt.Circle((0, 0), radius, color='black', fill=False, linestyle='--', transform=ellipse_transform)
ax.add_artist(ellipse)

# Draw black lines for the x and y axes
plt.axhline(0, color='black', linewidth=1.5)
plt.axvline(0, color='black', linewidth=1.5)

# Set axis limits and labels
plt.xlim(-0.7 * scale_x + offset_x, 0.7 * scale_x + offset_x)
plt.ylim(-0.7 * scale_y + offset_y, 0.7 * scale_y + offset_y)
plt.gca().set_aspect('equal', adjustable='box')

plt.xlabel('$M_x$ (G)', fontproperties=prop, color='black')
plt.ylabel('$M_y$ (G)', fontproperties=prop, color='black')

# Set the grid and background
plt.grid(True, color='grey', linestyle=':', linewidth=0.5)
plt.gca().set_facecolor('white')

# Show plot
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()