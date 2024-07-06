# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the file path
preprocessed_folder = os.path.expanduser("~/Documents/GitHub/Embedded-AI/data/LGHG2@n10C_to_25degC/Preprocessed")
train_file = os.path.join(preprocessed_folder, 'resampled_training_data.csv')

# Load the training data
train_df = pd.read_csv(train_file)

# Extract voltage and SOC for one discharge cycle
# Assuming the data is ordered, and one discharge cycle is continuous in the dataset
# You may need to adjust this if your data is organized differently
voltage = train_df['Voltage']
soc = train_df['SOC']

# Plot voltage vs SOC
plt.figure(figsize=(10, 6))
plt.plot(voltage, soc, label='Discharge Cycle')
plt.xlabel('Voltage (V)')
plt.ylabel('State of Charge (SOC)')
plt.title('Voltage vs SOC over One Discharge Cycle')
plt.legend()
plt.grid(True)
plt.show()