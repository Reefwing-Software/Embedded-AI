# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Define the categories and corresponding intelligence levels
categories = [
    "Single-Cell\n",
    "Plants\n",
    "Simple Multicellular\n",
    "Invertebrates\n",
    "Vertebrates\n",
    "Higher Vertebrates\n",
    "Humans\n"
]

intelligence_levels = [
    "\nMinimal",
    "\nLow",
    "\nBasic",
    "\nModerate",
    "\nIntermediate",
    "\nAdvanced",
    "\nVery High"
]

# Define the colors for the gradient
colors = plt.cm.viridis(np.linspace(0, 1, len(categories)))

# Create the plot
fig, ax = plt.subplots(figsize=(12, 2))

# Plot the gradient bar
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap('viridis'))

# Add the category labels below the bar
x_positions = np.linspace(0, 256, len(categories))
for i, category in enumerate(categories):
    ax.text(x_positions[i], -0.5, category, va='center', ha='center', color='black', fontweight='bold', fontsize=12)

# Add the intelligence level labels above the bar
for i, level in enumerate(intelligence_levels):
    ax.text(x_positions[i], 1.5, level, va='center', ha='center', color='black', fontweight='bold', fontsize=12)

# Hide the axes
ax.set_axis_off()

# Add a title
plt.title("Spectrum of Intelligence Across Different Life Forms\n", fontsize=14, fontweight='bold')

# Show the plot
plt.tight_layout()
plt.show()