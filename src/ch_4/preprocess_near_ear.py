# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
from sklearn.model_selection import train_test_split

# Define folder paths
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4")
preprocessed_folder = os.path.join(data_folder, 'Preprocessed')

# Ensure the preprocessed folder exists
os.makedirs(preprocessed_folder, exist_ok=True)

# Load datasets
openset_file = os.path.join(data_folder, 'openset.csv')
near_ear_file = os.path.join(data_folder, 'near_ear.csv')

# Read CSV files into pandas DataFrames
openset_df = pd.read_csv(openset_file)
near_ear_df = pd.read_csv(near_ear_file)

# Preprocessing function
def preprocess_and_normalize(df):
    # Check if required columns exist
    required_columns = ['aX', 'aY', 'aZ', 'proximity', 'time']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' is missing from the dataset.")
    
    # Remove rows with proximity = -1
    df = df[df['proximity'] != -1]
    
    # Drop the 'time' column
    df = df.drop(columns=['time'])
    
    # Normalize aX, aY, aZ to be between 0 and 1
    df[['aX', 'aY', 'aZ']] = (df[['aX', 'aY', 'aZ']] + 1) / 2
    
    # Normalize proximity to be between 0 and 1
    df['proximity'] = df['proximity'] / 255.0
    
    return df

# Preprocess datasets
openset_df = preprocess_and_normalize(openset_df)
near_ear_df = preprocess_and_normalize(near_ear_df)

# Combine and label datasets
openset_df['label'] = 0  # Label for openset
near_ear_df['label'] = 1  # Label for near-ear samples

combined_df = pd.concat([openset_df, near_ear_df], ignore_index=True)

# Shuffle and split datasets
train_val_df, test_df = train_test_split(combined_df, test_size=0.2, random_state=42, shuffle=True)
train_df, val_df = train_test_split(train_val_df, test_size=0.25, random_state=42, shuffle=True)  # 20% of 80% = 20%

# Save preprocessed datasets
train_file = os.path.join(preprocessed_folder, 'train.csv')
val_file = os.path.join(preprocessed_folder, 'val.csv')
test_file = os.path.join(preprocessed_folder, 'test.csv')

train_df.to_csv(train_file, index=False)
val_df.to_csv(val_file, index=False)
test_df.to_csv(test_file, index=False)

print(f"Preprocessed datasets saved to {preprocessed_folder}.")