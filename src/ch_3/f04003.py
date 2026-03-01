# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_4")
image_name = 'f04003.pdf'
image_path = os.path.join(image_folder, image_name)

# Example data
X = np.array([1, 2, 3, 4, 5])
Y = np.array([2, 4, 5, 4.5, 7])

# Calculate the line of best fit
coefficients = np.polyfit(X, Y, 1)
poly = np.poly1d(coefficients)
line_of_best_fit = poly(X)

# Plotting the data points
plt.scatter(X, Y, color='black', label='Data points')

# Plotting the line of best fit
plt.plot(X, line_of_best_fit, color='grey', linestyle='--', label='Line of best fit')

# Adding labels and title
plt.xlabel('X', fontproperties=prop)
plt.ylabel('Y', fontproperties=prop)
#plt.title('Linear regression', fontproperties=prop)
plt.legend(prop=prop)

# Save and show plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches="tight")
plt.show()