# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# Project: Proximity Detection Using ANNs

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from tensorflow.keras.models import load_model

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_4_v6")
image_name = 'f04007.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and load test data
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/Preprocessed")
test_file = os.path.join(data_folder, 'test.csv')
test_df = pd.read_csv(test_file)

# Separate features and labels
inputs_test = test_df[['aX', 'aY', 'aZ', 'proximity']].values
outputs_test = test_df['label'].values

# Load the trained model
model_save_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/Model")
model_path = os.path.join(model_save_folder, "near_ear_model.keras")
model = load_model(model_path)

# Use the model to predict the test inputs
predictions = model.predict(inputs_test)

# Print predictions and actual outputs
print("predictions =\n", np.round(predictions, decimals=3).flatten())
print("actual =\n", outputs_test)

# Plot the predictions versus the actual values in greyscale
plt.figure(figsize=(10, 6))
# plt.title('Test Data: Predicted vs Actual Values', fontproperties=prop)
plt.plot(outputs_test, '.', label='Actual', color='black', markersize=10)
plt.plot(predictions, '.', label='Predicted', color='grey', markersize=10)
plt.xlabel('Sample index', fontproperties=prop, color='black')
plt.ylabel('Output', fontproperties=prop, color='black')
plt.legend(prop=prop)
plt.grid(color='grey', linestyle='--', linewidth=0.5)
plt.tick_params(colors='black')
plt.gca().spines['bottom'].set_color('black')
plt.gca().spines['left'].set_color('black')
plt.gca().spines['top'].set_color('black')
plt.gca().spines['right'].set_color('black')

# Save and show the plot
os.makedirs(image_folder, exist_ok=True)
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()