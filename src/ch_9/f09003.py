# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pyquaternion import Quaternion
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import matplotlib.font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_9_final")
image_name = 'f09003.pdf'
image_path = os.path.join(image_folder, image_name)

# Define a quaternion (90-degree rotation about Z-axis)
q = Quaternion(axis=[0, 0, 1], degrees=90)

# Define a vector to rotate
vector = np.array([1, 0, 0])

# Rotate the vector using the quaternion
rotated_vector = q.rotate(vector)

# Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', fc='white')  # Set background to white
ax.quiver(0, 0, 0, *vector, color='black', label='Original vector')
ax.quiver(0, 0, 0, *rotated_vector, color='grey', label='Rotated vector')

# Customize axes limits and labels
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])
ax.set_xlabel('x', fontproperties=prop)
ax.set_ylabel('y', fontproperties=prop)
ax.set_zlabel('z', fontproperties=prop)

# Add legend with specified font
ax.legend(prop=prop)

# Save the plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()