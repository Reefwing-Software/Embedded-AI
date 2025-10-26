# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from scipy.ndimage import convolve

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_5")
image_name = 'f05008.pdf'
image_path = os.path.join(image_folder, image_name)

# Create a sample grayscale image (e.g., a 5x5 grid)
image = np.array([
    [1, 2, 3, 0, 0],
    [4, 5, 6, 0, 0],
    [7, 8, 9, 0, 0],
    [1, 2, 3, 0, 0],
    [4, 5, 6, 0, 0]
], dtype=np.float32)

# Define a simple convolution kernel (e.g., edge detection)
kernel = np.array([
    [-1, -1, -1],
    [ 0,  0,  0],
    [ 1,  1,  1]
], dtype=np.float32)

# Perform convolution
conv_output = convolve(image, kernel, mode='constant', cval=0.0)

# Apply max pooling (2x2 window, stride 2)
def max_pooling(input_array, pool_size):
    output_shape = (
        (input_array.shape[0] + pool_size - 1) // pool_size,
        (input_array.shape[1] + pool_size - 1) // pool_size
    )
    pooled = np.zeros(output_shape)
    for i in range(0, input_array.shape[0], pool_size):
        for j in range(0, input_array.shape[1], pool_size):
            pooled[i // pool_size, j // pool_size] = np.max(
                input_array[i:i + pool_size, j:j + pool_size]
            )
    return pooled

pooled_output = max_pooling(conv_output, pool_size=2)

# Plot the visualization
plt.figure(figsize=(12, 4))

# Original image
plt.subplot(1, 3, 1)
plt.title("Original image", fontproperties=prop)
plt.imshow(image, cmap="gray")
plt.colorbar()
plt.xlabel('x-axis', fontproperties=prop)
plt.ylabel('y-axis', fontproperties=prop)

# Convolved image
plt.subplot(1, 3, 2)
plt.title("After convolution", fontproperties=prop)
plt.imshow(conv_output, cmap="gray")
plt.colorbar()
plt.xlabel('x-axis', fontproperties=prop)

# Pooled image
plt.subplot(1, 3, 3)
plt.title("After max pooling", fontproperties=prop)
plt.imshow(pooled_output, cmap="gray")
plt.colorbar()
plt.xlabel('x-axis', fontproperties=prop)

# Save and show the plot
os.makedirs(image_folder, exist_ok=True)
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()