# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_4")
image_name = 'f04015.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the file paths
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/LGHG2@n10C_to_25degC")
preprocessed_folder = os.path.join(data_folder, 'Preprocessed')
train_file = os.path.join(preprocessed_folder, 'resampled_training_data.csv')
test_file_25deg = os.path.join(preprocessed_folder, 'resampled_test_data_25degC.csv')

# Load the training and test data
train_df = pd.read_csv(train_file)
test_df_25deg = pd.read_csv(test_file_25deg)

# Create subplots for side-by-side comparison
fig, axes = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={'wspace': 0.3})

# Plot the SOC for the training data
axes[0].plot(train_df['SOC'], label='Training data SOC', color='black')
axes[0].set_title('State of charge - training data', fontproperties=prop)
axes[0].set_xlabel('Time (s)', fontproperties=prop)
axes[0].set_ylabel('SOC', fontproperties=prop)
axes[0].legend(prop=prop)
axes[0].grid(True, linestyle='--', linewidth=0.5)

# Plot the SOC for the test data at 25 degrees C
axes[1].plot(test_df_25deg['SOC'], label='Test data SOC at 25°C', color='grey')
axes[1].set_title('State of charge - test data at 25°C', fontproperties=prop)
axes[1].set_xlabel('Time (s)', fontproperties=prop)
axes[1].set_ylabel('SOC', fontproperties=prop)
axes[1].legend(prop=prop)
axes[1].grid(True, linestyle='--', linewidth=0.5)

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()