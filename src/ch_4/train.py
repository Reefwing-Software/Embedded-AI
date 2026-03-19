# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# Project: Proximity Detection Using ANNs

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_4_v6")
image_name = 'f04006.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/Preprocessed")
model_save_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/Model")

# Load the preprocessed data
train_file = os.path.join(data_folder, 'train.csv')
val_file = os.path.join(data_folder, 'val.csv')
test_file = os.path.join(data_folder, 'test.csv')

train_df = pd.read_csv(train_file)
val_df = pd.read_csv(val_file)
test_df = pd.read_csv(test_file)

# Separate features and labels
X_train, y_train = train_df[['aX', 'aY', 'aZ', 'proximity']], train_df['label']
X_val, y_val = val_df[['aX', 'aY', 'aZ', 'proximity']], val_df['label']
X_test, y_test = test_df[['aX', 'aY', 'aZ', 'proximity']], test_df['label']

# Define the model
model = models.Sequential([
    layers.Input(shape=(4,)),             # Input layer for 4 features
    layers.Dense(8, activation='relu'),   # Hidden layer with 8 neurons
    layers.Dense(1, activation='sigmoid') # Output - binary classification
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=30,  # Number of epochs
    batch_size=32,  # Batch size
    verbose=1  # Show progress
)

# Evaluate on the test set
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Test Loss: {test_loss:.4f}")

# Save the model in the default TensorFlow format
os.makedirs(model_save_folder, exist_ok=True)
model_path = os.path.join(model_save_folder, "near_ear_model.keras")
model.save(model_path)
print(f"Model saved to {model_path}")

# Plotting accuracy and loss
history_dict = history.history
epochs = range(1, len(history_dict['loss']) + 1)

plt.figure(figsize=(12, 5))

# Plot accuracy
plt.subplot(1, 2, 1)
plt.plot(epochs, history_dict['accuracy'], label='Training accuracy', color='black', linestyle='solid')
plt.plot(epochs, history_dict['val_accuracy'], label='Validation accuracy', color='grey', linestyle='dashed')
# plt.title('Accuracy vs Epoch', fontproperties=prop)
plt.xlabel('Epoch', fontproperties=prop)
plt.ylabel('Accuracy', fontproperties=prop)
plt.legend(prop=prop)
plt.grid(color='grey', linestyle='--', linewidth=0.5)

# Plot loss
plt.subplot(1, 2, 2)
plt.plot(epochs, history_dict['loss'], label='Training loss', color='black', linestyle='solid')
plt.plot(epochs, history_dict['val_loss'], label='Validation loss', color='grey', linestyle='dashed')
# plt.title('Loss vs Epoch', fontproperties=prop)
plt.xlabel('Epoch', fontproperties=prop)
plt.ylabel('Loss', fontproperties=prop)
plt.legend(prop=prop)
plt.grid(color='grey', linestyle='--', linewidth=0.5)

# Save and show the plot
os.makedirs(image_folder, exist_ok=True)
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()