# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# ----------------------------------------------------------------------
# Font and paths
# ----------------------------------------------------------------------
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_9_final")
image_name = 'f09003.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name (not used here, but defined for completeness)
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_9")

# Make sure the image folder exists
os.makedirs(image_folder, exist_ok=True)

# ----------------------------------------------------------------------
# Quaternion example: rotation of 60 degrees about the z-axis
# ----------------------------------------------------------------------
angle_deg = 60.0
angle_rad = np.deg2rad(angle_deg)

# Axis of rotation (unit vector)
axis = np.array([0.0, 0.0, 1.0])

# Unit quaternion q = (w, x, y, z)
w = np.cos(angle_rad / 2.0)
x = axis[0] * np.sin(angle_rad / 2.0)
y = axis[1] * np.sin(angle_rad / 2.0)
z = axis[2] * np.sin(angle_rad / 2.0)
q = np.array([w, x, y, z])

# Original vector to be rotated
v = np.array([1.0, 0.0, 0.0])


# ----------------------------------------------------------------------
# Quaternion rotation: v' = q * v * q^{-1}
# ----------------------------------------------------------------------
def quat_multiply(q1, q2):
    """Hamilton product of two quaternions q1 and q2."""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w_ = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x_ = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y_ = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z_ = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w_, x_, y_, z_])


def rotate_vector(q, v):
    """Rotate 3D vector v with unit quaternion q."""
    v_quat = np.concatenate([[0.0], v])
    q_conj = np.array([q[0], -q[1], -q[2], -q[3]])
    return quat_multiply(quat_multiply(q, v_quat), q_conj)[1:]


v_rot = rotate_vector(q, v)

# ----------------------------------------------------------------------
# Figure and subplots
# ----------------------------------------------------------------------
plt.rcParams['pdf.fonttype'] = 42  # Better text in PDFs
plt.rcParams['ps.fonttype'] = 42

fig = plt.figure(figsize=(10, 3.5))

# ------------------- Panel (a): quaternion as a point in 3D -------------------
ax1 = fig.add_subplot(1, 3, 1, projection='3d')

# Draw a light grey sphere for visual context
u = np.linspace(0, 2 * np.pi, 40)
v_sphere = np.linspace(0, np.pi, 20)
xs = np.outer(np.cos(u), np.sin(v_sphere))
ys = np.outer(np.sin(u), np.sin(v_sphere))
zs = np.outer(np.ones_like(u), np.cos(v_sphere))
ax1.plot_surface(xs, ys, zs, rstride=2, cstride=2, linewidth=0.3,
                 edgecolor='0.85', facecolor='0.95', alpha=0.8)

# Plot the (x, y, z) part of the quaternion
ax1.scatter([x], [y], [z], s=40, c='0.1')

# Axes settings
ax1.set_xlabel('x', fontproperties=prop)
ax1.set_ylabel('y', fontproperties=prop)
ax1.set_zlabel('z', fontproperties=prop)
ax1.set_title('Quaternion spatial\ncomponents', fontproperties=prop)
ax1.set_box_aspect([1, 1, 1])
ax1.set_xlim([-1, 1])
ax1.set_ylim([-1, 1])
ax1.set_zlim([-1, 1])
ax1.grid(True, linestyle=':', linewidth=0.5, color='0.7')

# ------------------- Panel (b): axis–angle representation -------------------
ax2 = fig.add_subplot(1, 3, 2, projection='3d')

# Draw coordinate axes
axis_len = 1.2
ax2.quiver(0, 0, 0, axis_len, 0, 0, color='0.3', linewidth=1)
ax2.quiver(0, 0, 0, 0, axis_len, 0, color='0.5', linewidth=1)
ax2.quiver(0, 0, 0, 0, 0, axis_len, color='0.7', linewidth=1)

# Draw rotation axis (z-axis)
ax2.quiver(0, 0, 0, axis[0], axis[1], axis[2], color='0.1',
           linewidth=2, arrow_length_ratio=0.1)

# Draw an arc in the x–y plane showing the rotation angle
theta = np.linspace(0, angle_rad, 100)
arc_r = 0.9
arc_x = arc_r * np.cos(theta)
arc_y = arc_r * np.sin(theta)
arc_z = np.zeros_like(theta)
#ax2.plot(arc_x, arc_y, arc_z, color='0.2', linewidth=1.5)

# Mark the angle
mid_angle = angle_rad / 2.0
label_r = 1.0
ax2.text(label_r * np.cos(mid_angle),
         label_r * np.sin(mid_angle),
         0.0,
         r'$\theta = {:.0f}^\circ$'.format(angle_deg),
         fontproperties=prop,
         ha='center', va='center')

ax2.set_xlabel('x', fontproperties=prop)
ax2.set_ylabel('y', fontproperties=prop)
ax2.set_zlabel('z', fontproperties=prop)
ax2.set_title('Axis–angle view', fontproperties=prop)
ax2.set_box_aspect([1, 1, 1])
ax2.set_xlim([-1.2, 1.2])
ax2.set_ylim([-1.2, 1.2])
ax2.set_zlim([-1.2, 1.2])
ax2.grid(True, linestyle=':', linewidth=0.5, color='0.7')

# ------------------- Panel (c): action on a 3D vector -------------------
ax3 = fig.add_subplot(1, 3, 3, projection='3d')

# Draw coordinate axes
ax3.quiver(0, 0, 0, axis_len, 0, 0, color='0.3', linewidth=1)
ax3.quiver(0, 0, 0, 0, axis_len, 0, color='0.5', linewidth=1)
ax3.quiver(0, 0, 0, 0, 0, axis_len, color='0.7', linewidth=1)

# Original and rotated vectors (in the x–y plane)
ax3.quiver(0, 0, 0, v[0], v[1], v[2],
           color='0.4', linewidth=2, arrow_length_ratio=0.1)
ax3.quiver(0, 0, 0, v_rot[0], v_rot[1], v_rot[2],
           color='0.0', linewidth=2, arrow_length_ratio=0.1)

ax3.text(v[0], v[1], v[2], r'$\mathbf{v}$',
         fontproperties=prop, ha='left', va='bottom')
ax3.text(v_rot[0], v_rot[1], v_rot[2], r'$q\,\mathbf{v}\,q^{-1}$',
         fontproperties=prop, ha='left', va='bottom')

ax3.set_xlabel('x', fontproperties=prop)
ax3.set_ylabel('y', fontproperties=prop)
ax3.set_zlabel('z', fontproperties=prop)
ax3.set_title('Quaternion acting\non a vector', fontproperties=prop)
ax3.set_box_aspect([1, 1, 1])
ax3.set_xlim([-1.2, 1.2])
ax3.set_ylim([-1.2, 1.2])
ax3.set_zlim([-1.2, 1.2])
ax3.grid(True, linestyle=':', linewidth=0.5, color='0.7')

# ------------------- Panel labels -------------------
fig.text(0.03, 0.90, '(a)', fontproperties=prop)
fig.text(0.35, 0.90, '(b)', fontproperties=prop)
fig.text(0.67, 0.90, '(c)', fontproperties=prop)

# ----------------------------------------------------------------------
# Save and show
# ----------------------------------------------------------------------
#plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()