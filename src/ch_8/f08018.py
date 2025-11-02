# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_8")
image_name = 'f08018.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the function to approximate the integral
def f(x):
    return np.sin(x)

# Define the range and the number of rectangles for each approximation
x = np.linspace(0, 2 * np.pi, 1000)
n_values = [4, 8, 16, 32]

# Create a figure with 4 subplots
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.flatten()

# Define colors (grayscale) for the rectangles
colors = ['#444444', '#666666', '#888888', '#AAAAAA']

for i, n in enumerate(n_values):
    x_rect = np.linspace(0, 2 * np.pi, n + 1)
    y_rect = f((x_rect[:-1] + x_rect[1:]) / 2)
    width = (2 * np.pi) / n
    
    # Plot the function
    axes[i].plot(x, f(x), color='black', linewidth=2)
    
    # Plot the rectangles
    axes[i].bar(x_rect[:-1], y_rect, width=width, align='edge', edgecolor='black', color=colors[i], alpha=0.7)
    
    # Set title and labels using the custom font
    axes[i].set_title(f'{n} rectangles', fontsize=14, fontproperties=prop, color='black')
    axes[i].set_xlabel('x', fontsize=12, fontproperties=prop, color='black')
    axes[i].set_ylabel('f(x)', fontsize=12, fontproperties=prop, color='black')
    
    # Set the font properties for ticks
    axes[i].tick_params(axis='both', colors='black')
    axes[i].set_xticks(np.arange(0, 2 * np.pi + np.pi/2, np.pi/2))
    axes[i].set_xticklabels(['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'], fontproperties=prop)

# Adjust layout
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()