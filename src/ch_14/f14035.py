# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# Figure 14-35	High-side DAC voltage versus battery discharge current

import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_14_final")
image_name = 'f14035.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file paths
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_14")
file_path_3_7V = os.path.join(data_folder, "high_side_3_7V.txt")
file_path_4_2V = os.path.join(data_folder, "high_side_4_2V.txt")

# Function to read and parse data from a file
def read_data(file_path):
    dac_voltages = []
    sense_currents = []
    
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split(',')
            if len(parts) < 3:
                continue  # Skip malformed lines
            
            # Extract DAC Voltage and Sense Current values
            dac_voltage_str = parts[0].split(":")[1].strip().replace(" V", "")
            sense_current_str = parts[2].split(":")[1].strip().replace(" mA", "")
            
            try:
                dac_voltage = float(dac_voltage_str)
                sense_current = float(sense_current_str)
                dac_voltages.append(dac_voltage)
                sense_currents.append(sense_current)
            except ValueError:
                # Skip lines with conversion errors
                continue

    return dac_voltages, sense_currents

# Read data from both files
dac_voltages_3_7V, sense_currents_3_7V = read_data(file_path_3_7V)
dac_voltages_4_2V, sense_currents_4_2V = read_data(file_path_4_2V)

# Create the plot
plt.figure(figsize=(8, 6))

# Plot for 3.7V Battery
plt.plot(dac_voltages_3_7V, sense_currents_3_7V, color='black', label="3.7V battery")

# Plot for 4.2V Battery
plt.plot(dac_voltages_4_2V, sense_currents_4_2V, color='grey', linestyle='--', label="4.2V battery")

# Labels and title
plt.xlabel('DAC voltage (V)', fontproperties=prop)
plt.ylabel('Sense current (mA)', fontproperties=prop)
plt.title('Current versus DAC voltage', fontproperties=prop)

# Set gridlines
plt.xticks([i * 0.1 for i in range(40, 51)])  # Display x-axis labels every 0.1 V from 4 to 5 V
plt.yticks([i * 100 for i in range(0, 10)])   # Display y-axis labels up to 900 mA
plt.grid(which='both', linestyle='--', color='grey', alpha=0.7)

# Limit the x-axis to 4-5 V and y-axis to 900 mA
plt.xlim(4.0, 5.0)
plt.ylim(0, 900)

# Legend
plt.legend(prop=prop)

# Apply font to tick labels
plt.tick_params(colors='black', labelsize=10)
for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
    label.set_fontproperties(prop)

# Save and show the plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()