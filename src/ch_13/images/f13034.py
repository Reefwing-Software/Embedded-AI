# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# Figure 14-34	The STP60N MOSFET Transfer Characteristic (VBAT = 4.2 V)

import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_13_v3")
image_name = 'f13034.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file path
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_13")
file_name = "transfer_characteristics.txt"
file_path = os.path.join(data_folder, file_name)

# Threshold voltage (Vt) - adjust as needed
Vt = 4.2

# Lists to hold Vgs and Ids data
vgs_values = []
ids_values = []

# Parse the data file
with open(file_path, 'r') as file:
    for line in file:
        parts = line.split(',')
        if len(parts) < 2:
            continue  # Skip malformed lines
        
        # Extract Vgs and Ids values
        vgs_str = parts[0].split(":")[1].strip().replace(" V", "")
        ids_str = parts[1].split(":")[1].strip().replace(" mA", "")
        
        try:
            vgs = float(vgs_str)
            ids = float(ids_str)
            vgs_values.append(vgs)
            ids_values.append(ids)
        except ValueError:
            # Skip lines with conversion errors
            continue

# Create the plot
plt.figure(figsize=(8, 6))

# Plot Vgs vs Ids
plt.plot(vgs_values, ids_values, color='black', linestyle='-', marker='o', label="Vgs versus Ids")

# Draw a vertical line for Vt
plt.axvline(Vt, color='grey', linestyle='--', label=f"Threshold voltage (Vt = {Vt} V)")

# Labels and title
plt.xlabel('Vgs (V)', fontproperties=prop)
plt.ylabel('Ids (mA)', fontproperties=prop)
plt.title('Transfer characteristics (Vgs versus Ids)', fontproperties=prop)

# Add gridlines
plt.grid(which='both', linestyle='--', color='grey', alpha=0.7)

# Add a legend
plt.legend(prop=prop)

# Apply font to tick labels
plt.tick_params(colors='black', labelsize=10)
for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
    label.set_fontproperties(prop)

# Save and show the plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()