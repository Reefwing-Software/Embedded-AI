# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import numpy as np

# Load the data
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)
data = pd.read_csv(file_path)

# Function to detect missing values
def detect_missing_values(df):
    missing_values = df.isnull().sum()
    total_cells = np.product(df.shape)
    total_missing = missing_values.sum()
    
    print(f"Total cells: {total_cells}")
    print(f"Total missing values: {total_missing}")
    print(f"Percentage of missing values: {(total_missing/total_cells) * 100:.2f}%")
    print("\nMissing values per column:")
    print(missing_values)

# Function to detect near-zero values
def detect_near_zero_values(df, threshold=0.001):
    near_zero_values = (df < threshold).sum()
    total_cells = np.product(df.shape)
    total_near_zero = near_zero_values.sum()
    
    print(f"Total cells: {total_cells}")
    print(f"Total near-zero values (less than {threshold}): {total_near_zero}")
    print(f"Percentage of near-zero values: {(total_near_zero/total_cells) * 100:.2f}%")
    print("\nNear-zero values per column:")
    print(near_zero_values)

# Detect missing values in the dataset
detect_missing_values(data)

# Detect near-zero values in the dataset
detect_near_zero_values(data)