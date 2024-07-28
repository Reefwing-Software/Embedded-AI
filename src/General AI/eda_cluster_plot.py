# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/AI-Advances/articles/exploratory_data_analysis/Preprocessed")
file_name = 'resampled_training_data.csv'
file_path = os.path.join(data_folder, file_name)

# Load the data
data = pd.read_csv(file_path)

# Select relevant variables for clustering
features = ['Voltage', 'Current', 'SOC']
X = data[features]

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Perform K-Means clustering
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# Add cluster labels to the data
data['Cluster'] = clusters

# Create 3D scatter plot of the clusters
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

sc = ax.scatter(data['Voltage'], data['Current'], data['SOC'], c=data['Cluster'], cmap='viridis', alpha=0.7)

ax.set_title('3D Scatter Plot of Clusters')
ax.set_xlabel('Voltage')
ax.set_ylabel('Current')
ax.set_zlabel('SOC')

# Add a color bar to show cluster labels
cbar = plt.colorbar(sc)
cbar.set_label('Cluster')

plt.show()