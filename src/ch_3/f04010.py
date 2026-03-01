# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_4")
image_name = 'f04010.pdf'
image_path = os.path.join(image_folder, image_name)

# Constants
R = 110e3  # Resistance in ohms
C = 14e-12  # Capacitance in farads
T = R * C  # Time constant
Vc = 5  # Fully charged voltage

# Time constants to show on the x-axis
time_multiples = np.linspace(0, 5, 500)  # Time multiples of T
time = time_multiples * T

# Capacitor charging formulas
voltage = Vc * (1 - np.exp(-time_multiples))  # Voltage across the capacitor
current = (Vc / R) * np.exp(-time_multiples)  # Current through the circuit

# Plotting the charge curve
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot capacitor voltage
ax1.plot(time_multiples, voltage, label='Capacitor voltage', color='black', linestyle='solid')
ax1.set_xlabel("Time (T)", fontproperties=prop)
ax1.set_ylabel("Capacitor voltage (V)", fontproperties=prop)
ax1.set_ylim(0, Vc + 0.5)
ax1.set_xticks([0.7, 1, 2, 3, 4, 5])
ax1.set_xticklabels(["0.7T", "1T", "2T", "3T", "4T", "5T"], fontproperties=prop)
ax1.set_yticks([0.5 * Vc, 0.63 * Vc, Vc])
ax1.set_yticklabels(["0.5Vc", "0.63Vc", "Vc"], fontproperties=prop)
ax1.set_xlim(left=0)
ax1.grid(True, linestyle="--", linewidth=0.5)

# Highlight 0.5Vc, 0.63Vc, and Vc
ax1.axhline(0.5 * Vc, color='grey', linestyle='--', linewidth=0.8)
ax1.axhline(0.63 * Vc, color='grey', linestyle='--', linewidth=0.8)
ax1.axhline(Vc, color='grey', linestyle='--', linewidth=0.8)

# Add vertical line at 4T
ax1.axvline(4, color='black', linestyle='dotted', linewidth=2)

# Label "Transient Period" and "Steady State"
plt.text(2, Vc + 0.2, "Transient period", fontproperties=prop, horizontalalignment='center')
plt.text(4.5, Vc + 0.2, "Steady state", fontproperties=prop, horizontalalignment='center')

# Plot current on secondary y-axis
ax2 = ax1.twinx()
ax2.plot(time_multiples, current, label='Current', color='grey', linestyle='dashed')
ax2.set_ylabel("Current (uA)", fontproperties=prop)
ax2.set_ylim(0, (Vc / R) + 1e-6)

# Add legend
ax1.legend(loc="lower left", prop=prop)
ax2.legend(loc="lower right", prop=prop)

# Save and show the plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches="tight")
plt.show()