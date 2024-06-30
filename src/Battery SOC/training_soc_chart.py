# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the file paths
preprocessed_folder = os.path.expanduser("~/Documents/GitHub/Embedded-AI/data/LGHG2@n10C_to_25degC/preprocessed")
train_file = os.path.join(preprocessed_folder, 'resampled_training_data.csv')
test_file_25deg = os.path.join(preprocessed_folder, 'resampled_test_data_25degC.csv')

# Load the training and test data
train_df = pd.read_csv(train_file)
test_df_25deg = pd.read_csv(test_file_25deg)

# Plot the SOC for the training data
plt.figure(figsize=(12, 6))
plt.plot(train_df['SOC'], label='Training Data SOC')
plt.title('State of Charge (SOC) - Training Data')
plt.xlabel('Time (s)')
plt.ylabel('SOC')
plt.legend()
plt.grid(True)
plt.show()

# Plot the SOC for the test data at 25 degrees C
plt.figure(figsize=(12, 6))
plt.plot(test_df_25deg['SOC'], label='Test Data SOC at 25°C', color='orange')
plt.title('State of Charge (SOC) - Test Data at 25°C')
plt.xlabel('Time (s)')
plt.ylabel('SOC')
plt.legend()
plt.grid(True)
plt.show()