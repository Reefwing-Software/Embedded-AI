# Copyright (c) 2026 David Such
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
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_8_v4")
image_name = 'f08014.pdf'
image_path = os.path.join(image_folder, image_name)

# IMU data
data = {
    "Sensor": [
        "BMI270", "BMI270", "BMI270", "BMI270", "BMI270", "BMI270", "BMI270", "BMI270", "BMI270",
        "BMI270", "BMI270", "BMI270", "BMI270", "BMI270", "BMI270", "BMI270", "BMI270", "BMI270",
        "LSM9DS1", "LSM9DS1", "LSM9DS1", "LSM9DS1", "LSM9DS1", "LSM9DS1", "LSM9DS1", "LSM9DS1", "LSM9DS1",
        "LSM9DS1", "LSM9DS1", "LSM9DS1", "LSM9DS1", "LSM9DS1", "LSM9DS1", "LSM9DS1", "LSM9DS1", "LSM9DS1",
        "MPU6050", "MPU6050", "MPU6050", "MPU6050", "MPU6050", "MPU6050", "MPU6050", "MPU6050", "MPU6050",
        "MPU6050", "MPU6050", "MPU6050", "MPU6050", "MPU6050", "MPU6050", "MPU6050", "MPU6050", "MPU6050"
    ],
    "Type": [
        "Roll", "Roll", "Roll", "Roll", "Roll", "Roll", "Roll", "Roll", "Roll",
        "Pitch", "Pitch", "Pitch", "Pitch", "Pitch", "Pitch", "Pitch", "Pitch", "Pitch",
        "Roll", "Roll", "Roll", "Roll", "Roll", "Roll", "Roll", "Roll", "Roll",
        "Pitch", "Pitch", "Pitch", "Pitch", "Pitch", "Pitch", "Pitch", "Pitch", "Pitch",
        "Pitch", "Pitch", "Pitch", "Pitch", "Pitch", "Pitch", "Pitch", "Pitch", "Pitch",
        "Roll", "Roll", "Roll", "Roll", "Roll", "Roll", "Roll", "Roll", "Roll"
    ],
    "Angle": [
        -80, -60, -40, -20, 0, 20, 40, 60, 80,
        -80, -60, -40, -20, 0, 20, 40, 60, 80,
        -80, -60, -40, -20, 0, 20, 40, 60, 80,
        -80, -60, -40, -20, 0, 20, 40, 60, 80,
        -80, -60, -40, -20, 0, 20, 40, 60, 80,
        -80, -60, -40, -20, 0, 20, 40, 60, 80
    ],
    "Calculated Roll": [
        -78.35, -58.63, -39.32, -19.73, 0.01, 19.71, 39.46, 59.47, 80.06,
        0.50, 0.39, 0.50, 0.08, -0.02, -0.18, -0.31, -0.37, 2.42,
        -78.92, -59.13, -39.45, -19.62, 0.00, 19.84, 39.69, 60.32, 80.81,
        0.51, 0.62, 0.26, 0.26, 0.02, 0.31, 0.82, 2.02, 10.20,
        14.43, 6.29, 3.17, 1.49, 0.07, -0.06, -1.29, -0.15, 5.65,
        -74.40, -35.55, -28.88, -15.21, -2.71, 14.60, 32.51, 50.33, 68.42
    ],
    "Calculated Pitch": [
        4.13, 1.70, 0.97, 0.24, 0.02, -0.40, -0.62, -0.67, 0.72,
        -77.75, -58.56, -39.03, -19.60, 0.00, 20.41, 40.58, 62.10, 83.62,
        1.84, 0.80, 0.37, 0.17, -0.01, 0.13, 0.01, -0.78, -3.71,
        -81.25, -61.37, -41.08, -20.85, 0.01, 21.07, 42.26, 62.80, 83.97,
        -73.25, -54.20, -36.69, -18.00, 0.25, 18.34, 37.49, 57.40, 76.84,
        10.01, 2.69, -1.15, -2.65, -1.42, -0.73, 0.49, 2.47, 6.66
    ]
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Calculate expected values
df["True Roll"] = np.where(df["Type"] == "Roll", df["Angle"], 0.0)
df["True Pitch"] = np.where(df["Type"] == "Pitch", df["Angle"], 0.0)

# Compute errors
df["Roll Error"] = df["Calculated Roll"] - df["True Roll"]
df["Pitch Error"] = df["Calculated Pitch"] - df["True Pitch"]
df["Roll RMSE"] = df["Roll Error"] ** 2
df["Pitch RMSE"] = df["Pitch Error"] ** 2

# Group by sensor for RMSE calculation
rmse_df = df.groupby("Sensor").agg(
    Roll_RMSE=("Roll RMSE", lambda x: np.sqrt(x.mean())),
    Pitch_RMSE=("Pitch RMSE", lambda x: np.sqrt(x.mean()))
).reset_index()

# Plot setup
fig, axes = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={"wspace": 0.4})
colors = plt.cm.Greys(np.linspace(0.3, 0.8, len(df["Sensor"].unique())))

# First Plot: Error
for sensor, color in zip(df["Sensor"].unique(), colors):
    subset = df[df["Sensor"] == sensor]
    axes[0].plot(subset["Angle"], subset["Roll Error"], label=f"{sensor} - Roll", color=color, linestyle="--")
    axes[0].plot(subset["Angle"], subset["Pitch Error"], label=f"{sensor} - Pitch", color=color)

axes[0].set_title("IMU accuracy (error versus angle)", fontproperties=prop)
axes[0].set_xlabel("Angle (degrees)", fontproperties=prop)
axes[0].set_ylabel("Error (degrees)", fontproperties=prop)
axes[0].grid(True, linestyle="--", linewidth=0.5)
axes[0].legend(prop=prop)

# Second Plot: RMSE
axes[1].bar(rmse_df["Sensor"], rmse_df["Roll_RMSE"], label="Roll RMSE", alpha=0.7, color="grey")
axes[1].bar(rmse_df["Sensor"], rmse_df["Pitch_RMSE"], label="Pitch RMSE", alpha=0.4, color="black")
axes[1].set_title("RMSE by sensor", fontproperties=prop)
axes[1].set_ylabel("RMSE (degrees)", fontproperties=prop)
axes[1].grid(True, linestyle="--", linewidth=0.5)
axes[1].legend(prop=prop)

# Save and show plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches="tight")
plt.show()