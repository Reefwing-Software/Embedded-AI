# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_8")
image_name = 'f08017.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_8")
file_name = "accelerometer_axis_angles.csv"
file_path = os.path.join(data_folder, file_name)

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Calculate RMSE for each roll and pitch against the actual values
rmse_roll_1 = np.sqrt(np.mean((df['Roll-1'] - df['Roll-Actual']) ** 2))
rmse_pitch_1 = np.sqrt(np.mean((df['Pitch-1'] - df['Pitch-Actual']) ** 2))

rmse_roll_2 = np.sqrt(np.mean((df['Roll-2'] - df['Roll-Actual']) ** 2))
rmse_pitch_2 = np.sqrt(np.mean((df['Pitch-2'] - df['Pitch-Actual']) ** 2))

rmse_roll_3 = np.sqrt(np.mean((df['Roll-3'] - df['Roll-Actual']) ** 2))
rmse_pitch_3 = np.sqrt(np.mean((df['Pitch-3'] - df['Pitch-Actual']) ** 2))

# Prepare data for the bar chart
rmse_values = [rmse_roll_1, rmse_roll_2, rmse_roll_3, rmse_pitch_1, rmse_pitch_2, rmse_pitch_3]
labels = ['Roll 1-axis', 'Roll 2-axis', 'Roll 3-axis', 'Pitch 1-axis', 'Pitch 2-axis', 'Pitch 3-axis']

# Print the RMSE results
print(f"RMSE for Roll-1 (Single Axis Roll): {rmse_roll_1:.4f} degrees")
print(f"RMSE for Pitch-1 (Single Axis Pitch): {rmse_pitch_1:.4f} degrees")

print(f"RMSE for Roll-2 (Two Axis Roll): {rmse_roll_2:.4f} degrees")
print(f"RMSE for Pitch-2 (Two Axis Pitch): {rmse_pitch_2:.4f} degrees")

print(f"RMSE for Roll-3 (Three Axis Roll): {rmse_roll_3:.4f} degrees")
print(f"RMSE for Pitch-3 (Three Axis Pitch): {rmse_pitch_3:.4f} degrees")

# Grayscale colors
colors = ['#444444', '#666666', '#888888', '#AAAAAA', '#CCCCCC', '#EEEEEE']

# Create a bar chart
plt.figure(figsize=(10, 6))
plt.bar(labels, rmse_values, color=colors)

# Set the font properties for labels and title
plt.xlabel('Calculation method', fontsize=14, color='black', fontproperties=prop)
plt.ylabel('RMSE (degrees)', fontsize=14, color='black', fontproperties=prop)
# plt.title('RMSE of Roll and Pitch Calculations', fontsize=16, fontweight='bold', fontproperties=prop)

# Set the font properties for ticks
plt.xticks(fontproperties=prop, color='black')
plt.yticks(fontproperties=prop, color='black')

# Show the plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()