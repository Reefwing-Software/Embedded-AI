# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_4")
image_name = 'f04011.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4")
file_name = "battery_capacity.csv"
file_path = os.path.join(data_folder, file_name)

# Read the CSV file into a DataFrame
data = pd.read_csv(file_path)

# Extract the capacity and 3S data
capacity = data["Capacity %"]
voltage_3s = data["3S"]

# Plot the 3S curve with reversed x-axis
plt.figure(figsize=(10, 6))
plt.plot(capacity, voltage_3s, color='grey', linestyle='solid', label='3S battery')
plt.scatter(capacity, voltage_3s, color='grey', label='Data points', s=50)

# Adding labels, title, and legend
plt.xlabel('Capacity (%)', fontproperties=prop)
plt.ylabel('Voltage (V)', fontproperties=prop)
# plt.title('Battery Voltage vs Capacity', fontproperties=prop)
plt.gca().invert_xaxis()  # Reverse the x-axis
plt.legend(prop=prop)
plt.grid(True, linestyle="--", linewidth=0.5)

# Save and show plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()