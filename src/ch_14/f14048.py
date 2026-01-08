# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_14_final")
image_name = 'f14048.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_14")
file_name = "cycle.txt"
file_path = os.path.join(data_folder, file_name)

# Function to parse the data file and extract time and voltage
def parse_data(file_path):
    elapsed_minutes = []
    voltages = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        start_time = None  # To calculate elapsed time

        for line in lines:
            parts = line.strip().split('|')
            if len(parts) < 2:
                continue  # Skip malformed lines
            
            # Extract timestamp and voltage
            timestamp_str = parts[0].strip().split()[0]  # Assume ISO 8601 format (e.g., 2024-11-10T10:18:13)
            voltage_str = parts[1].strip()

            try:
                # Parse the timestamp
                current_time = datetime.fromisoformat(timestamp_str)

                # Extract voltage value and convert from mV to V
                voltage = float(voltage_str.split()[0]) / 1000.0
                voltages.append(voltage)

                # Calculate elapsed time in minutes
                if start_time is None:
                    start_time = current_time
                    elapsed_minutes.append(0)
                else:
                    elapsed_seconds = (current_time - start_time).total_seconds()
                    elapsed_minutes.append(elapsed_seconds / 60)  # Convert seconds to minutes
            except ValueError:
                continue  # Skip lines with invalid data

    return elapsed_minutes, voltages

# Parse the data
time_minutes, voltages = parse_data(file_path)

# Create the plot
plt.figure(figsize=(8, 6))

plt.plot(time_minutes, voltages, color='black', label="Battery voltage")

# Add labels, title, and legend
plt.xlabel('Time (minutes)', fontproperties=prop)
plt.ylabel('Voltage (V)', fontproperties=prop)
plt.title('Battery voltage versus time', fontproperties=prop)

# Add gridlines
plt.grid(which='both', linestyle='--', color='grey', alpha=0.7)

# Add font properties to tick labels
plt.tick_params(colors='black', labelsize=10)
for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
    label.set_fontproperties(prop)

# Save the plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()