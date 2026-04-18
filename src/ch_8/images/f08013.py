# Copyright (c) 2026 David Such
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
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_8_v4")
image_name = 'f08013.pdf'
image_path = os.path.join(image_folder, image_name)

data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_8")

# List of files to analyze
files = [
    "lsm9ds1_static_pitch.txt", 
    "lsm9ds1_static_roll.txt", 
    "bmi270_static_pitch.txt", 
    "bmi270_static_roll.txt", 
    "mpu6050_static_pitch.txt", 
    "mpu6050_static_roll.txt"
]

# Adjust pandas display options
pd.set_option("display.max_columns", None)  
pd.set_option("display.width", 0)  
pd.set_option("display.float_format", "{:.4f}".format)

# Function to calculate theoretical values based on angle
def calculate_theoretical_values(angle, orientation):
    rad_angle = np.radians(angle)
    if orientation == "Pitch":
        return np.sin(rad_angle), 0, np.cos(rad_angle)
    elif orientation == "Roll":
        return 0, np.sin(rad_angle), np.cos(rad_angle)

# Function to read and process a single file
def process_file(file_path):
    data = []
    offsets = None
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("Offsets:"):
                offsets = line
            elif line and not line.startswith("Angle"):
                values = line.split(',')
                angle = int(values[0])
                ax = float(values[1])
                ay = float(values[2])
                az = float(values[3])
                norm = np.sqrt(ax**2 + ay**2 + az**2)
                data.append([angle, ax, ay, az, norm])
    
    df = pd.DataFrame(data, columns=["Angle", "ax", "ay", "az", "Norm"])
    
    orientation = os.path.basename(file_path).split("_")[2].replace(".txt", "").capitalize()
    theoretical = [calculate_theoretical_values(angle, orientation) for angle in df["Angle"]]
    df["Theoretical_ax"], df["Theoretical_ay"], df["Theoretical_az"] = zip(*theoretical)
    df["Deviation_ax"] = df["ax"] - df["Theoretical_ax"]
    df["Deviation_ay"] = df["ay"] - df["Theoretical_ay"]
    df["Deviation_az"] = df["az"] - df["Theoretical_az"]
    df["Total_Deviation"] = (
        df["Deviation_ax"].abs() + df["Deviation_ay"].abs() + df["Deviation_az"].abs()
    )
    
    sensor_type = os.path.basename(file_path).split("_")[0].upper()
    df["Sensor"] = sensor_type  # Add Sensor column to the data

    summary = df.groupby("Angle").agg(
        Mean_Total_Deviation=("Total_Deviation", "mean"),
    ).reset_index()
    
    summary["Sensor"] = sensor_type  # Add Sensor column to the summary
    
    return df, summary

# Process all files and aggregate results
deviation_data = []
aggregated_summary = []
for file_name in files:
    file_path = os.path.join(data_folder, file_name)
    df, summary = process_file(file_path)
    deviation_data.append(df)
    aggregated_summary.append(summary)

# Combine results into DataFrames
deviation_data = pd.concat(deviation_data, ignore_index=True)

# Aggregate across orientations for each IMU
aggregated_summary = (
    deviation_data.groupby(["Sensor", "Angle"])
    .agg(
        Mean_Total_Deviation=("Total_Deviation", "mean"),
    )
    .reset_index()
)

# Calculate RMSE and MAE per sensor
error_summary = deviation_data.groupby("Sensor").agg(
    RMSE_ax=("Deviation_ax", lambda x: np.sqrt((x**2).mean())),
    RMSE_ay=("Deviation_ay", lambda x: np.sqrt((x**2).mean())),
    RMSE_az=("Deviation_az", lambda x: np.sqrt((x**2).mean())),
    MAE_ax=("Deviation_ax", lambda x: x.abs().mean()),
    MAE_ay=("Deviation_ay", lambda x: x.abs().mean()),
    MAE_az=("Deviation_az", lambda x: x.abs().mean())
).reset_index()

# Save data to CSV
aggregated_summary_path = os.path.join(data_folder, "imu_aggregated_deviation_summary.csv")
error_summary_path = os.path.join(data_folder, "imu_error_summary.csv")
aggregated_summary.to_csv(aggregated_summary_path, index=False)
error_summary.to_csv(error_summary_path, index=False)

# Create the plots
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Greyscale color palette
num_sensors = len(aggregated_summary["Sensor"].unique())
colors = plt.cm.Greys_r(np.linspace(0.3, 0.8, num_sensors))

# First plot: Total deviation vs angle for each sensor (aggregated across orientations)
for idx, sensor in enumerate(aggregated_summary["Sensor"].unique()):
    subset = aggregated_summary[aggregated_summary["Sensor"] == sensor]
    axes[0].plot(
        subset["Angle"], 
        subset["Mean_Total_Deviation"], 
        label=sensor,
        color=colors[idx]
    )
axes[0].set_title("Total deviation versus angle (aggregated)", fontproperties=prop)
axes[0].set_xlabel("Angle (degrees)", fontproperties=prop)
axes[0].set_ylabel("Total deviation (m/s^2)", fontproperties=prop)
axes[0].legend(prop=prop)
axes[0].grid(True, linestyle="--", linewidth=0.5)

# Second plot: MAE for ax, ay, az per sensor
width = 0.2
x = np.arange(len(error_summary["Sensor"]))
axes[1].bar(x - width, error_summary["MAE_ax"], width, label="ax MAE", color=colors[0])
axes[1].bar(x, error_summary["MAE_ay"], width, label="ay MAE", color=colors[1])
axes[1].bar(x + width, error_summary["MAE_az"], width, label="az MAE", color=colors[2])
axes[1].set_xticks(x)
axes[1].set_xticklabels(error_summary["Sensor"])
axes[1].set_title("MAE for ax, ay, az by sensor", fontproperties=prop)
axes[1].set_ylabel("MAE (m/s^2)", fontproperties=prop)
axes[1].legend(prop=prop)
axes[1].grid(True, linestyle="--", linewidth=0.5)

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches="tight")
plt.show()

# Print error summary table
print("Error Summary Table:")
print(error_summary)