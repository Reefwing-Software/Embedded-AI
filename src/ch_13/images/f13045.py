# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import datetime as dt

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_13_v3")
image_name = 'f13045.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file paths
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_13")
discharge_file_path = os.path.join(data_folder, "discharge_150mA.txt")
charge_file_path = os.path.join(data_folder, "charge_500mA.txt")

def parse_data(file_path):
    times = []
    voltages = []
    start_time = None

    with open(file_path, 'r') as file:
        for line in file:
            # Skip empty or malformed lines
            if not line.strip():
                continue

            parts = line.split()
            if len(parts) < 4:
                continue

            timestamp_str = parts[0]  # ISO timestamp
            voltage_str = parts[3]  # Voltage in mV

            try:
                # Parse timestamp and convert to elapsed minutes
                timestamp = dt.datetime.fromisoformat(timestamp_str)
                if start_time is None:
                    start_time = timestamp
                elapsed_time = (timestamp - start_time).total_seconds() / 60.0

                # Parse voltage, remove 'mV', and convert to V
                voltage = int(voltage_str.replace("mV", "")) / 1000.0

                times.append(elapsed_time)
                voltages.append(voltage)

            except (ValueError, IndexError):
                # Skip line if there's an error in parsing
                continue

    return times, voltages

# Read and parse discharge and charge data
discharge_times, discharge_voltages = parse_data(discharge_file_path)
charge_times, charge_voltages = parse_data(charge_file_path)

# Create the plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

# Discharge curve
ax1.plot(discharge_times, discharge_voltages, color='black')
ax1.set_title('Battery discharge curve (150 mA)', fontproperties=prop)
ax1.set_xlabel('Time (minutes)', fontproperties=prop)
ax1.set_ylabel('Voltage (V)', fontproperties=prop)

# Charge curve
ax2.plot(charge_times, charge_voltages, color='black')
ax2.set_title('Battery charge curve (500 mA)', fontproperties=prop)
ax2.set_xlabel('Time (minutes)', fontproperties=prop)

# Apply font to tick labels
for ax in (ax1, ax2):
    ax.tick_params(colors='black', labelsize=10)
    ax.grid(which='major', linestyle=':', linewidth=0.8, alpha=0.7)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(prop)

# Show the plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()