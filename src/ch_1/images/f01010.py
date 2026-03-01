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

# Define the image folder and file name for the hardware trade-off plot
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_1")
if not os.path.exists(image_folder):
    os.makedirs(image_folder)
image_name = 'f01010.pdf'
image_path = os.path.join(image_folder, image_name)

# Define a piecewise function for performance:
# For energy efficiency (x) values less than or equal to the optimum (here x = 5), performance increases rapidly.
# Beyond x = 5, performance gently declines, reflecting diminishing returns.
# Parameters:
#   - A maximum performance is nearly reached at x = 5.
#   - For x > 5, a small linear decline (slope = 0.5) is applied.
x = np.linspace(0, 10, 200)  # Energy efficiency (relative units)
y = np.piecewise(x, 
                 [x <= 5, x > 5],
                 [lambda x: 25 * (1 - np.exp(-0.8 * x)),
                  lambda x: 25 * (1 - np.exp(-0.8 * 5)) - 0.5 * (x - 5)])
# At x=5, 25*(1 - exp(-4)) ≈ 24.54, so performance peaks around this value and then declines gently.

# Plot the improved trade-off curve
plt.figure(figsize=(8, 6))
plt.plot(x, y, color='black', linewidth=2)
#plt.title("Energy Efficiency vs. Performance Trade-off (Improved Model)", fontproperties=prop)
plt.xlabel("Energy efficiency (relative units)", fontproperties=prop)
plt.ylabel("Performance (relative units)", fontproperties=prop)
plt.grid(True, linestyle='-', linewidth=0.5, color='gray')

# Remove axis numbers by hiding tick labels
plt.xticks([])  
plt.yticks([])

plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()