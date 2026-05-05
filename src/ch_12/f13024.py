# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import re
import json
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the font path
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define file paths
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_13/")
file_name = "job_27200445_stdout_log.json"  # Updated to .json
file_path = os.path.join(data_folder, file_name)

image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_13_final")
image_name = 'f13024.pdf'
image_path = os.path.join(image_folder, image_name)

# Initialize lists to hold data
epochs = []
train_loss = []
val_loss = []
train_acc = []
val_acc = []

# Updated regex pattern to match logs
metrics_pattern = re.compile(
    r"120/120 - \d+s - loss: ([\d.]+) - accuracy: ([\d.]+) - val_loss: ([\d.]+) - val_accuracy: ([\d.]+)"
)
epoch_pattern = re.compile(r"Epoch (\d+)/30")

# Read and parse the JSON file
with open(file_path, 'r') as file:
    log_json = json.load(file)
    stdout_logs = log_json.get("stdout", [])  # Extract 'stdout' logs

    current_epoch = None  # Track the current epoch
    for entry in stdout_logs:
        data_line = entry.get("data", "")  # Extract 'data' field
        
        # Match epoch number
        epoch_match = epoch_pattern.search(data_line)
        if epoch_match:
            current_epoch = int(epoch_match.group(1))  # Update current epoch
        
        # Match metrics
        metrics_match = metrics_pattern.search(data_line)
        if metrics_match and current_epoch is not None:
            epochs.append(current_epoch)
            train_loss.append(float(metrics_match.group(1)))
            train_acc.append(float(metrics_match.group(2)))
            val_loss.append(float(metrics_match.group(3)))
            val_acc.append(float(metrics_match.group(4)))
            current_epoch = None  # Reset epoch after logging

# Plot the data
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Loss plot
axes[0].plot(epochs, train_loss, label="Training loss", linestyle='-', color='black')
axes[0].plot(epochs, val_loss, label="Validation loss", linestyle='--', color='grey')
axes[0].set_xlabel("Epoch", fontproperties=prop)
axes[0].set_ylabel("Loss", fontproperties=prop)
axes[0].set_title("Epoch vs loss", fontproperties=prop)
axes[0].grid(True)
axes[0].legend(prop=prop)

# Accuracy plot
axes[1].plot(epochs, train_acc, label="Training accuracy", linestyle='-', color='black')
axes[1].plot(epochs, val_acc, label="Validation accuracy", linestyle='--', color='grey')
axes[1].set_xlabel("Epoch", fontproperties=prop)
axes[1].set_ylabel("Accuracy", fontproperties=prop)
axes[1].set_title("Epoch vs accuracy", fontproperties=prop)
axes[1].grid(True)
axes[1].legend(prop=prop)

# Layout, save, and show
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()