# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
from scipy.stats import skew, kurtosis

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)

# Load the data
data = pd.read_csv(file_path)

# Calculate Central Tendency
mean = data.mean()
median = data.median()
mode_value = data.mode().iloc[0]

# Calculate Dispersion
data_max = data.max()
data_min = data.min()
data_range = data_max - data_min
variance = data.var()
std_deviation = data.std()

# Calculate Distribution Shape
skewness = data.apply(lambda x: skew(x.dropna()))
kurt = data.apply(lambda x: kurtosis(x.dropna()))

# Column names for which to calculate frequency distribution
columns = ['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current', 'SOC']

# Display the results
print("\nCentral Tendency:")
print(f"Mean:\n{mean}\n")
print(f"Median:\n{median}\n")
print(f"Mode:\n{mode_value}\n")

print("Dispersion:")
print(f"Maximum:\n{data_max}\n")
print(f"Minimum:\n{data_min}\n")
print(f"Range:\n{data_range}\n")
print(f"Variance:\n{variance}\n")
print(f"Standard Deviation:\n{std_deviation}\n")

print("Distribution Shape:")
print(f"Skewness:\n{skewness}\n")
print(f"Kurtosis:\n{kurt}\n")

# Calculate and display frequency distribution for each column
print("Frequency Distribution:")
for col in columns:
    print(f"\n{col}:")
    print(data[col].value_counts())