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

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_9_final")
image_name = 'f09020.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and ISM330BX file path
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_9")
ism330bx_file = os.path.join(data_folder, "ism330bx_static_roll.csv")

# IMU data for BMI270, LSM9DS1, and MPU6050
data = {
    "Sensor": ["BMI270"] * 9 + ["LSM9DS1"] * 9 + ["MPU6050"] * 9,
    "Angle": [-80, -60, -40, -20, 0, 20, 40, 60, 80] * 3,
    "Calculated Roll": [
        -78.35, -58.63, -39.32, -19.73, 0.01, 19.71, 39.46, 59.47, 80.06,
        -78.92, -59.13, -39.45, -19.62, 0.00, 19.84, 39.69, 60.32, 80.81,
        -74.40, -35.55, -28.88, -15.21, -2.71, 14.60, 32.51, 50.33, 68.42
    ]
}

# Convert BMI270, LSM9DS1, and MPU6050 data to DataFrame
imu_roll_df = pd.DataFrame(data)

# Calculate True Roll and Errors for BMI270, LSM9DS1, and MPU6050
imu_roll_df.loc[:, "True Roll"] = imu_roll_df["Angle"]
imu_roll_df.loc[:, "Roll Error"] = imu_roll_df["Calculated Roll"] - imu_roll_df["True Roll"]
imu_roll_df.loc[:, "Roll RMSE"] = imu_roll_df["Roll Error"] ** 2

# Calculate RMSE for BMI270, LSM9DS1, and MPU6050
rmse_values = imu_roll_df.groupby("Sensor")["Roll RMSE"].mean().apply(np.sqrt)

# Load ISM330BX data
ism330bx_data = pd.read_csv(ism330bx_file)

# Extract relevant columns and add sensor identifier
ism330bx_roll_df = ism330bx_data[["Angle", "roll"]].rename(columns={"roll": "Calculated Roll"}).copy()
ism330bx_roll_df["Sensor"] = "ISM330BX"

# Calculate True Roll and Errors for ISM330BX
ism330bx_roll_df.loc[:, "True Roll"] = ism330bx_roll_df["Angle"]
ism330bx_roll_df.loc[:, "Roll Error"] = ism330bx_roll_df["Calculated Roll"] - ism330bx_roll_df["True Roll"]
ism330bx_roll_df.loc[:, "Roll RMSE"] = ism330bx_roll_df["Roll Error"] ** 2

# Append ISM330BX data to IMU DataFrame
imu_roll_df = pd.concat([imu_roll_df, ism330bx_roll_df], ignore_index=True)

# Calculate RMSE for all sensors
rmse_values = imu_roll_df.groupby("Sensor")["Roll RMSE"].mean().apply(np.sqrt)

# Plot setup
fig, axes = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={"wspace": 0.4})

# Define greyscale colors and line styles
num_sensors = imu_roll_df["Sensor"].nunique()
colors = plt.cm.Greys_r(np.linspace(0.3, 0.8, num_sensors))
line_styles = {
    "ISM330BX": "solid",
    "MPU6050": "dashed",
    "BMI270": "solid",
    "LSM9DS1": "dashdot"
}

# First Plot: Error
for idx, sensor in enumerate(imu_roll_df["Sensor"].unique()):
    subset = imu_roll_df[imu_roll_df["Sensor"] == sensor]
    axes[0].plot(
        subset["Angle"], subset["Roll Error"],
        label=f"{sensor} Roll Error",
        color=colors[idx],
        linestyle=line_styles[sensor]
    )
axes[0].set_title("Roll accuracy (error versus angle)", fontproperties=prop)
axes[0].set_xlabel("Angle (degrees)", fontproperties=prop)
axes[0].set_ylabel("Error (degrees)", fontproperties=prop)
axes[0].grid(True, linestyle="--", linewidth=0.5)
axes[0].legend(prop=prop)

# Second Plot: RMSE
axes[1].bar(
    rmse_values.index, rmse_values.values, color=colors[:len(rmse_values)], alpha=0.7
)
axes[1].set_title("Roll RMSE by sensor", fontproperties=prop)
axes[1].set_ylabel("RMSE (degrees)", fontproperties=prop)
axes[1].grid(True, linestyle="--", linewidth=0.5)

# Save and show plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches="tight")
plt.show()

# Print RMSE values
print("Roll RMSE values:")
print(rmse_values)