# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_7")
file_name = "accelerometer_axis_angles.csv"
file_path = os.path.join(data_folder, file_name)

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Filter the data to only include rows where actual roll or pitch is 0
zero_roll_rows = df[df['Roll-Actual'] == 0]
zero_pitch_rows = df[df['Pitch-Actual'] == 0]

# Calculate the average bias offset for each calculation type for Roll
roll_bias_1 = zero_roll_rows['Roll-1'].mean()
roll_bias_2 = zero_roll_rows['Roll-2'].mean()
roll_bias_3 = zero_roll_rows['Roll-3'].mean()

# Calculate the average bias offset for each calculation type for Pitch
pitch_bias_1 = zero_pitch_rows['Pitch-1'].mean()
pitch_bias_2 = zero_pitch_rows['Pitch-2'].mean()
pitch_bias_3 = zero_pitch_rows['Pitch-3'].mean()

# Print the results
print(f"Average Bias Offset for Roll-1 (Single Axis Roll): {roll_bias_1:.4f} degrees")
print(f"Average Bias Offset for Roll-2 (Two Axis Roll): {roll_bias_2:.4f} degrees")
print(f"Average Bias Offset for Roll-3 (Three Axis Roll): {roll_bias_3:.4f} degrees")
print(f"Average Bias Offset for Pitch-1 (Single Axis Pitch): {pitch_bias_1:.4f} degrees")
print(f"Average Bias Offset for Pitch-2 (Two Axis Pitch): {pitch_bias_2:.4f} degrees")
print(f"Average Bias Offset for Pitch-3 (Three Axis Pitch): {pitch_bias_3:.4f} degrees")