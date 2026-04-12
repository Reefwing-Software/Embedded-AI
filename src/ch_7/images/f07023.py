# Copyright (c) 2026 David Such
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
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_7_v4")
image_name = 'f07023.pdf'
image_path = os.path.join(image_folder, image_name)

# Generate the ideal sphere data
phi = np.linspace(0, np.pi, 180)
theta = np.linspace(0, 2 * np.pi, 360)
phi, theta = np.meshgrid(phi, theta)
radius = 0.5

# Cartesian coordinates for the sphere
X = radius * np.sin(phi) * np.cos(theta)
Y = radius * np.sin(phi) * np.sin(theta)
Z = radius * np.cos(phi)

# Add random noise to simulate real sensor readings
noise_level = 0.01
X_noisy = X + np.random.normal(0, noise_level, X.shape)
Y_noisy = Y + np.random.normal(0, noise_level, Y.shape)
Z_noisy = Z + np.random.normal(0, noise_level, Z.shape)

# Apply soft iron distortion by scaling the axes differently
scale_x = 1.2  # Stretching factor for X
scale_y = 0.8  # Compression factor for Y
scale_z = 1.0  # No change for Z in this example

X_noisy *= scale_x
Y_noisy *= scale_y
Z_noisy *= scale_z

# Apply rotation to simulate tilt
rotation_angle = 20  # Degrees
rotation_radians = np.deg2rad(rotation_angle)

# Rotation matrix for Z axis (can apply different rotations for X, Y if needed)
rotation_matrix = np.array([[np.cos(rotation_radians), -np.sin(rotation_radians), 0],
                            [np.sin(rotation_radians),  np.cos(rotation_radians), 0],
                            [0, 0, 1]])

# Rotate the data
X_rotated, Y_rotated, Z_rotated = np.dot(rotation_matrix, np.array([X_noisy.flatten(), Y_noisy.flatten(), Z_noisy.flatten()]))

# Reshape back to original shape
X_rotated = X_rotated.reshape(X.shape)
Y_rotated = Y_rotated.reshape(Y.shape)
Z_rotated = Z_rotated.reshape(Z.shape)

# Apply hard iron distortion by offsetting the data
offset_x = 0.2
offset_y = 0.2
offset_z = 0.2
X_rotated += offset_x
Y_rotated += offset_y
Z_rotated += offset_z

# Create the 3D plot
fig = plt.figure(figsize=(11, 11))
ax = fig.add_subplot(111, projection='3d')

# Plot the distorted sphere
ax.scatter(X_rotated, Y_rotated, Z_rotated, color='grey', s=1)

# Plot mesh lines on the ellipsoid to visualize its 3D structure
ax.plot_wireframe(X_rotated, Y_rotated, Z_rotated, color='black', linewidth=0.1, alpha=0.1)

# Plot reference lines for the axes
# ax.plot([0, 1], [0, 0], [0, 0], color='black', linewidth=2)  # X-axis
# ax.plot([0, 0], [0, 1], [0, 0], color='black', linewidth=2)  # Y-axis
# ax.plot([0, 0], [0, 0], [0, 1], color='black', linewidth=2)  # Z-axis

# Set labels and title using the custom font
ax.set_xlabel('Mx (G)', fontproperties=prop)
ax.set_ylabel('My (G)', fontproperties=prop)
ax.set_zlabel('Mz (G)', fontproperties=prop)

# Show plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()