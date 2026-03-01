# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import cm
import numpy as np

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_9_final")
image_name = 'f09007.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_9")
file_name = "filterTest.txt"
file_path = os.path.join(data_folder, file_name)

# Filter mapping
filter_mapping = {
    "0": "Madgwick",
    "1": "Mahony",
    "2": "Complementary",
    "3": "Classic",
    "4": "EKF",
    "5": "None"
}

# Initialize variables
filter_data = []
invalid_data_count = []

# Read the file
with open(file_path, 'r') as file:
    lines = file.readlines()
    current_filter = None
    noise_condition = None
    for line in lines:
        line = line.strip()
        # Updated parsing to handle filter ID with noise conditions
        # Updated parsing to handle noise condition properly
        if line.startswith("Testing filter:"):
            # Extract the filter ID and the noise condition
            parts = line.split(":")[1].strip().split()
            filter_id = parts[0]  # Extract the base filter ID (e.g., "0")
            noise_condition = " ".join(parts[1:])  # Extract the noise condition (e.g., "without noise" or "with noise")
            
            # Retrieve the filter name and append only the noise condition
            current_filter = filter_mapping.get(filter_id, f"Unknown ({filter_id})")
        elif line.startswith("Time,Roll Error,Pitch Error,Yaw Error"):
            # Skip header line
            continue
        elif line and current_filter is not None:
            # Parse the data line and handle invalid values
            values = line.split(",")
            try:
                time = float(values[0])
                roll_error = float(values[1]) if values[1] != "ovf" else float('nan')
                pitch_error = float(values[2]) if values[2] != "ovf" else float('nan')
                yaw_error = float(values[3]) if values[3] != "ovf" else float('nan')
                filter_data.append({
                    "Filter": current_filter,
                    "Noise Condition": noise_condition,
                    "Time": time,
                    "Roll Error": roll_error,
                    "Pitch Error": pitch_error,
                    "Yaw Error": yaw_error
                })
                # Count invalid data
                if values[1] == "ovf" or values[2] == "ovf" or values[3] == "ovf":
                    invalid_data_count.append({
                        "Filter": current_filter,
                        "Noise Condition": noise_condition,
                        "Invalid Field": "Roll" if values[1] == "ovf" else "Pitch" if values[2] == "ovf" else "Yaw",
                        "Time": time
                    })
            except ValueError:
                # Skip invalid lines
                print(f"Skipping invalid line: {line}")

# Adjust pandas display options to show all columns
pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.width", 0)  # Automatically adjust the display width to terminal size
pd.set_option("display.float_format", "{:.3f}".format)  # Display numbers to 3 decimal places

# Convert to a DataFrame
df = pd.DataFrame(filter_data)

# Drop rows with NaN (optional, if you want to exclude invalid values)
df = df.dropna()

# Create an invalid data summary
invalid_df = pd.DataFrame(invalid_data_count)

if not invalid_df.empty:
    # Group by filter and noise condition and count invalid entries
    invalid_summary = invalid_df.groupby(["Filter", "Noise Condition"]).size().reset_index(name="Invalid Data Count")
else:
    # If there are no invalid entries, create an empty DataFrame with the same structure
    invalid_summary = pd.DataFrame(columns=["Filter", "Noise Condition", "Invalid Data Count"])

# Summary statistics
summary = df.groupby(["Filter", "Noise Condition"]).agg(
    Mean_Roll_Error=("Roll Error", "mean"),
    Std_Roll_Error=("Roll Error", "std"),
    Mean_Pitch_Error=("Pitch Error", "mean"),
    Std_Pitch_Error=("Pitch Error", "std"),
    Mean_Yaw_Error=("Yaw Error", "mean"),
    Std_Yaw_Error=("Yaw Error", "std"),
).reset_index()

# Merge invalid data counts into the main summary
summary = pd.merge(summary, invalid_summary, on=["Filter", "Noise Condition"], how="left")
summary["Invalid Data Count"] = summary["Invalid Data Count"].fillna(0).astype(int)

# Save the summary table
summary_table_path = os.path.join(data_folder, "filter_summary.csv")
summary.to_csv(summary_table_path, index=False)

# Plot Roll Error over Time for each filter
plt.figure(figsize=(10, 6))

# Exclude the NONE filter from the DataFrame
df_filtered = df[df["Filter"] != "None"]

# Update the number of filters for the new DataFrame
num_filters = len(df_filtered["Filter"].unique())
#colors = cm.Greys_r(np.linspace(0.3, 0.8, num_filters))  # Shades of grey
colors = plt.cm.tab10(np.linspace(0, 1, num_filters))
line_styles = ['-', '--', '-.', ':']  # Cyclic line styles

# Plot Roll Error over Time for each filter
for idx, filter_name in enumerate(df_filtered["Filter"].unique()):
    subset = df_filtered[(df_filtered["Filter"] == filter_name) & (df_filtered["Noise Condition"] == "without noise")]
    plt.plot(
        subset["Time"], 
        subset["Roll Error"], 
        label=f"{filter_name} (no noise)",
        linestyle=line_styles[idx % len(line_styles)],
        color=colors[idx % len(colors)]
    )
    subset = df_filtered[(df_filtered["Filter"] == filter_name) & (df_filtered["Noise Condition"] == "with noise")]
    plt.plot(
        subset["Time"], 
        subset["Roll Error"], 
        label=f"{filter_name} (with noise)",
        linestyle=line_styles[(idx + 1) % len(line_styles)],
        color=colors[idx % len(colors)]
    )

# Add plot details
plt.title("Roll error over time for different filters", fontproperties=prop)
plt.xlabel("Time (s)", fontproperties=prop)
plt.ylabel("Roll error (degrees)", fontproperties=prop)
plt.ylim(bottom=-100, top=150)   # Set y-axis limits 
plt.legend(prop=prop, loc="lower right")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches="tight")
plt.show()

# Print the summary table to the console
print("Filter Performance Summary:")
print(summary)