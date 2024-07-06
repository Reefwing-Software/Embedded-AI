# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the file path
preprocessed_folder = os.path.expanduser("~/Documents/GitHub/Embedded-AI/data/LGHG2@n10C_to_25degC/Preprocessed")
train_file = os.path.join(preprocessed_folder, 'resampled_training_data.csv')

# Load the training data
train_df = pd.read_csv(train_file)

# Extract voltage and SOC for plotting
voltage = train_df['Voltage']
soc = train_df['SOC']

# Plot SOC vs Voltage
plt.figure(figsize=(10, 6))
plt.plot(soc, voltage, label='Charge/Discharge Cycles')
plt.xlabel('State of Charge (SOC)')
plt.ylabel('Voltage (V)')
plt.title('Voltage vs SOC over Multiple Cycles')
plt.gca().invert_xaxis()  # Invert the x-axis
plt.legend()
plt.grid(True)
plt.show()