import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)

# Load the data
data = pd.read_csv(file_path)

# Define the indices for each temperature segment
idx_ranges = {
    '0C': (1, 184257),
    '10C': (184258, 337973),
    '25C': (337974, 510530),
    '-10C': (510531, 669956)
}

# Create temperature indicators
data['Temperature_0C'] = ((data.index >= 1) & (data.index <= 184257)).astype(int)
data['Temperature_10C'] = ((data.index >= 184258) & (data.index <= 337973)).astype(int)
data['Temperature_25C'] = ((data.index >= 337974) & (data.index <= 510530)).astype(int)
data['Temperature_-10C'] = ((data.index >= 510531) & (data.index <= 669956)).astype(int)

# Perform EDA and normalization separately for each segment
scaler = StandardScaler()
for temp, (start_idx, end_idx) in idx_ranges.items():
    segment_data = data.iloc[start_idx-1:end_idx]
    
    # Plot histograms for each feature within the segment
    segment_data.hist(bins=50, figsize=(15, 10))
    plt.suptitle(f'Feature Distributions at {temp}')
    plt.show()
    
    # Normalize features within the segment
    features = ['Voltage', 'Current', 'Temperature', 'Average Voltage', 'Average Current', 'SOC']
    segment_data[features] = scaler.fit_transform(segment_data[features])