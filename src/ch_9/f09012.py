# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and data folder
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_9_final")
image_name = 'f09012.pdf'
image_path = os.path.join(image_folder, image_name)

data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_9")

# List of files to analyze
files = [
    "lsm9ds1_static_pitch.txt", 
    "lsm9ds1_static_roll.txt", 
    "bmi270_static_pitch.txt", 
    "bmi270_static_roll.txt", 
    "mpu6050_static_pitch.txt", 
    "mpu6050_static_roll.txt"
]

# Adjust pandas display options to show all columns
pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.width", 0)  # Automatically adjust the display width to terminal size
pd.set_option("display.float_format", "{:.4f}".format)  # Display numbers to 4 decimal places

# Initialize an empty DataFrame to store all results
results = []

# Function to read and process a single file
def process_file(file_path):
    data = []
    offsets = None
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("Offsets:"):
                offsets = line  # Store offsets for information
            elif line and not line.startswith("Angle"):
                # Parse angle and accelerometer data
                values = line.split(',')
                angle = int(values[0])
                ax = float(values[1])
                ay = float(values[2])
                az = float(values[3])
                norm = np.sqrt(ax**2 + ay**2 + az**2)
                data.append([angle, ax, ay, az, norm])
    
    # Create a DataFrame for the file
    df = pd.DataFrame(data, columns=["Angle", "ax", "ay", "az", "Norm"])
    
    # Calculate mean and standard deviation for each angle
    summary = df.groupby("Angle").agg(
        Mean_ax=("ax", "mean"),
        Std_ax=("ax", "std"),
        Mean_ay=("ay", "mean"),
        Std_ay=("ay", "std"),
        Mean_az=("az", "mean"),
        Std_az=("az", "std"),
        Mean_Norm=("Norm", "mean"),
        Std_Norm=("Norm", "std")
    ).reset_index()
    
    # Add sensor information
    sensor_type = os.path.basename(file_path).split("_")[0].upper()
    orientation = os.path.basename(file_path).split("_")[2].replace(".txt", "").capitalize()
    summary["Sensor"] = sensor_type
    summary["Orientation"] = orientation
    summary["Offsets"] = offsets
    
    return summary

# Process all files and append results
for file_name in files:
    file_path = os.path.join(data_folder, file_name)
    results.append(process_file(file_path))

# Combine all results into a single DataFrame
final_results = pd.concat(results, ignore_index=True)

# Calculate overall summary per IMU
imu_summary = final_results.groupby("Sensor").agg(
    Mean_Norm=("Mean_Norm", "mean"),
    Mean_SD=("Std_Norm", "mean"),
    Mean_Error=("Mean_Norm", lambda x: abs(x - 1).mean())  # Mean error assuming norm should be close to 1
).reset_index()

# Save the summaries to CSV
output_csv_path_summary = os.path.join(data_folder, "imu_summary.csv")
imu_summary.to_csv(output_csv_path_summary, index=False)

# Save the results to a CSV file
output_csv_path = os.path.join(data_folder, "imu_static_angles_summary.csv")
final_results.to_csv(output_csv_path, index=False)

# Create the figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# First plot: Norm of Acceleration Vector vs. Angle
num_lines = len(final_results["Sensor"].unique()) * len(final_results["Orientation"].unique())
colors = plt.cm.Greys_r(np.linspace(0.3, 0.8, num_lines))  # Greyscale colors

for idx, (sensor, orientation) in enumerate(final_results.groupby(["Sensor", "Orientation"])):
    subset = final_results[(final_results["Sensor"] == sensor[0]) & (final_results["Orientation"] == sensor[1])]
    axes[0].errorbar(
        subset["Angle"], 
        subset["Mean_Norm"], 
        yerr=subset["Std_Norm"], 
        label=f"{sensor[0]} ({sensor[1]})",
        color=colors[idx % len(colors)]
    )

axes[0].set_title("Norm of acceleration vector versus angle for different IMUs", fontproperties=prop)
axes[0].set_xlabel("Angle (degrees)", fontproperties=prop)
axes[0].set_ylabel("Norm of acceleration (m/s^2)", fontproperties=prop)
axes[0].legend(prop=prop, loc="lower left")
axes[0].grid(True, which="both", linestyle="--", linewidth=0.5)

# Second plot: Mean Norm vs Angle for each sensor (aggregating roll and pitch)
aggregated_results = final_results.groupby(["Sensor", "Angle"]).agg(
    Mean_Norm=("Mean_Norm", "mean"),
    Std_Norm=("Std_Norm", "mean")
).reset_index()

# Use greyscale for the second plot as well
sensor_colors = plt.cm.Greys_r(np.linspace(0.3, 0.8, len(aggregated_results["Sensor"].unique())))

for idx, sensor in enumerate(aggregated_results["Sensor"].unique()):
    subset = aggregated_results[aggregated_results["Sensor"] == sensor]
    axes[1].errorbar(
        subset["Angle"], 
        subset["Mean_Norm"], 
        yerr=subset["Std_Norm"], 
        label=sensor,
        color=sensor_colors[idx % len(sensor_colors)]  # Greyscale
    )

axes[1].set_title("Mean norm versus angle for different sensors", fontproperties=prop)
axes[1].set_xlabel("Angle (degrees)", fontproperties=prop)
axes[1].set_ylabel("Mean norm (m/s^2)", fontproperties=prop)
axes[1].legend(prop=prop, loc="lower left")
axes[1].grid(True, which="both", linestyle="--", linewidth=0.5)

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches="tight")
plt.show()

# Print the summary table to the console
print("Final Results:")
print(final_results)

print("\nIMU Summary:")
print(imu_summary)