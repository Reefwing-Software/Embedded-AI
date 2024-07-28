# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

# Load the data
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)
data = pd.read_csv(file_path)

# Extract the 'Voltage' column
voltage_data = data['Voltage']

# Generate a QN plot for the voltage data
plt.figure(figsize=(8, 6))
stats.probplot(voltage_data, dist="norm", plot=plt)
plt.title('Quantile-Normal (QN) Plot for Voltage Data')
plt.xlabel('Theoretical Quantiles')
plt.ylabel('Sample Quantiles')
plt.grid(True)
plt.show()