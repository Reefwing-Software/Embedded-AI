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
import matplotlib.font_manager as fm

from mpl_toolkits.mplot3d import Axes3D

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_6")
image_name = 'f06017c.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP/eda/Preprocessed")
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

# Use a grayscale colormap for the clusters
sc = ax.scatter(data['Voltage'], data['Current'], data['SOC'], c=data['Cluster'], cmap='Greys', alpha=0.7)

# Apply the custom font properties to the axis labels
ax.set_xlabel('Voltage', fontproperties=prop, color='black')
ax.set_ylabel('Current', fontproperties=prop, color='black')
ax.set_zlabel('SOC', fontproperties=prop, color='black')

# Add a color bar to show cluster labels in grayscale
cbar = plt.colorbar(sc)
cbar.set_label('Cluster', fontproperties=prop, color='black')

# Set the desired view angle
ax.view_init(elev=20, azim=133)

# Save the figure
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()