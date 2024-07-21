# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
from scipy.stats import skew, kurtosis, mode

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)

# Load the data
data = pd.read_csv(file_path)

# Calculate Central Tendency
mean = data.mean()
median = data.median()
mode_value = mode(data, nan_policy='omit').mode[0]

# Calculate Dispersion
data_range = data.max() - data.min()
variance = data.var()
std_deviation = data.std()

# Calculate Distribution Shape
skewness = data.apply(lambda x: skew(x.dropna()))
kurt = data.apply(lambda x: kurtosis(x.dropna()))

# Frequency Distribution (for simplicity, showing value counts for the first column)
frequency_distribution = data.iloc[:, 0].value_counts()

# Display the results
print("Central Tendency:")
print(f"Mean:\n{mean}\n")
print(f"Median:\n{median}\n")
print(f"Mode:\n{mode_value}\n")

print("Dispersion:")
print(f"Range:\n{data_range}\n")
print(f"Variance:\n{variance}\n")
print(f"Standard Deviation:\n{std_deviation}\n")

print("Distribution Shape:")
print(f"Skewness:\n{skewness}\n")
print(f"Kurtosis:\n{kurt}\n")

print("Frequency Distribution (first column):")
print(frequency_distribution)