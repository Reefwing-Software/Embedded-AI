# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import numpy as np

# Define paths
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/LGHG2@n10C_to_25degC")
preprocessed_folder = os.path.join(data_folder, 'Preprocessed')

# Resampled test data file names
test_files = {
    'n10degC': 'resampled_test_data_n10degC.csv',
    '0degC': 'resampled_test_data_0degC.csv',
    '10degC': 'resampled_test_data_10degC.csv',
    '25degC': 'resampled_test_data_25degC.csv'
}

# Feature names
feature_names = ['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current']

# Select the test file to process (e.g., n10degC)
selected_test_file = test_files['n10degC']  # Adjust this to choose a different file
test_path = os.path.join(preprocessed_folder, selected_test_file)

# Load the test data
test_df = pd.read_csv(test_path)

# Extract Voltage and SOC
voltage = test_df['Voltage'].values  # Normalized voltage values (0 to 1)
soc = test_df['SOC'].values  # Normalized SOC values (0 to 1)

# Constants for scaling back to the 3S battery range
VOLTAGE_MIN = 982  # 9.82V in *100 format
VOLTAGE_MAX = 1260  # 12.6V in *100 format
SOC_MIN = 0
SOC_MAX = 100  # SOC in percentage

# Scale normalized Voltage and SOC back to the original range
voltage_rescaled = ((voltage * (VOLTAGE_MAX - VOLTAGE_MIN)) + VOLTAGE_MIN).astype(int)
soc_rescaled = ((soc * (SOC_MAX - SOC_MIN)) + SOC_MIN).astype(int)

# Sample 100 evenly spaced values
indices = np.linspace(0, len(voltage_rescaled) - 1, 100, dtype=int)
voltage_sample = voltage_rescaled[indices]
soc_sample = soc_rescaled[indices]

# Combine into a formatted C++ array with 5 groups per line
cpp_array = "const int32_t voltage_soc[100][2] = {\n"

line = []
for i, (v, s) in enumerate(zip(voltage_sample, soc_sample)):
    line.append(f"{{{v}, {s}}}")
    if (i + 1) % 5 == 0:  # Add a newline after every 5 groups
        cpp_array += "    " + ", ".join(line) + ",\n"
        line = []

# Add any remaining items (if the total count isn't a multiple of 5)
if line:
    cpp_array += "    " + ", ".join(line) + ",\n"

# Close the array
cpp_array = cpp_array.rstrip(",\n") + "\n};"

# Ensure terminal output is not truncated
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Print the formatted C++ array
print(cpp_array)