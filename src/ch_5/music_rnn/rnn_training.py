# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import pickle
import datetime
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from pathlib import Path
from tensorflow.keras import layers

# Define the custom loss function
def mse_with_positive_pressure(y_true: tf.Tensor, y_pred: tf.Tensor):
    mse = (y_true - y_pred) ** 2
    positive_pressure = 10 * tf.maximum(-y_pred, 0.0)
    return tf.reduce_mean(mse + positive_pressure)

# Create a unique log directory for each run
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
log_dir = f"./logs/{current_time}"

# Define the input shape and model parameters
seq_length = 50
input_shape = (seq_length, 3)
learning_rate = 0.001

# Load scaling factors using pickle
data_folder = Path("~/Documents/GitHub/NSP-Embedded-AI/data/ch_5/maestro").expanduser()
dividers_path = data_folder / "dividers.pkl"
with open(dividers_path, 'rb') as f:
    dividers = pickle.load(f)

step_divider = dividers['step_divider']
duration_divider = dividers['duration_divider']
pitch_min = dividers['pitch_min']
pitch_max = dividers['pitch_max']

# Create the model
inputs = tf.keras.Input(input_shape)
x = tf.keras.layers.LSTM(128)(inputs)

outputs = {
    'pitch': tf.keras.layers.Dense(128, name='pitch')(x),
    'step': layers.Lambda(lambda x: x / step_divider, name='step')(
        layers.Dense(1, activation='relu', name='step_dense')(x)
    ),
    'duration': layers.Lambda(lambda x: x / duration_divider, name='duration')(
        layers.Dense(1, activation='relu', name='duration_dense')(x)
    )
}

model = tf.keras.Model(inputs, outputs, name="music_rnn_model")

# Define the loss functions
loss = {
    'pitch': tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    'step': mse_with_positive_pressure,
    'duration': mse_with_positive_pressure,
}

# Define loss weights to balance contributions
loss_weights = {
    'pitch': 0.05,
    'step': 1.0,
    'duration': 1.0,
}

optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

# Compile the model
model.compile(
    loss=loss, 
    loss_weights=loss_weights, 
    optimizer=optimizer,
    metrics={'pitch': tf.keras.metrics.SparseCategoricalAccuracy(name='accuracy')}
)
model.summary()

# Load the sequenced datasets
train_dataset_path = data_folder / "train_seq_ds_50.tfrecord"
val_dataset_path = data_folder / "val_seq_ds_50.tfrecord"
test_dataset_path = data_folder / "test_seq_ds_50.tfrecord"

train_ds = tf.data.Dataset.load(str(train_dataset_path))
val_ds = tf.data.Dataset.load(str(val_dataset_path))
test_ds = tf.data.Dataset.load(str(test_dataset_path))

# Define callbacks
callbacks = [
    tf.keras.callbacks.ModelCheckpoint(
        filepath='./training_checkpoints/ckpt_{epoch}.weights.h5',  
        save_weights_only=True),
    tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',  # Monitor validation loss for early stopping
        patience=5,
        verbose=1,
        restore_best_weights=True),
    tf.keras.callbacks.TensorBoard(log_dir=log_dir)
]

print(f"Logs will be saved in: {log_dir}")

# Train the model
epochs = 50
history = model.fit(
    train_ds,
    validation_data=val_ds,  # Use validation dataset
    epochs=epochs,
    callbacks=callbacks,
)

# Evaluate the model on the test dataset
test_metrics = model.evaluate(test_ds, return_dict=True)
print(f"Test loss: {test_metrics['loss']}")
print(f"Test pitch accuracy: {test_metrics['pitch_accuracy']}")

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_5")
image_name = 'f05022_new.pdf'
image_path = os.path.join(image_folder, image_name)

# Create the directory if it doesn't exist
os.makedirs(image_folder, exist_ok=True)

# Plot the training and validation metrics
plt.figure(figsize=(16, 6))

# Subplot 1: Loss vs Epoch
plt.subplot(1, 2, 1)
plt.plot(history.epoch, history.history['loss'], label='Training Loss', color='black')  # Grayscale
plt.plot(history.epoch, history.history['val_loss'], label='Validation Loss', color='gray')  # Grayscale
plt.xlabel('Epochs', fontproperties=prop)
plt.ylabel('Loss', fontproperties=prop)
plt.title('Training and Validation Loss Over Time', fontproperties=prop)
plt.grid(color='gray', linestyle='--', linewidth=0.5)  
plt.legend(prop=prop)

# Subplot 2: Accuracy vs Epoch
plt.subplot(1, 2, 2)

# Plot training and validation accuracy over epochs
plt.plot(history.epoch, history.history.get('pitch_accuracy', []), label='Training Pitch Accuracy', color='black')  # Grayscale
plt.plot(history.epoch, history.history.get('val_pitch_accuracy', []), label='Validation Pitch Accuracy', color='gray')  # Grayscale
test_pitch_accuracy = test_metrics.get('pitch_accuracy', 0)
plt.axhline(y=test_pitch_accuracy, color='lightgray', linestyle='--', label=f'Test Pitch Accuracy ({test_pitch_accuracy:.2f})')
plt.xlabel('Epochs', fontproperties=prop)
plt.ylabel('Accuracy', fontproperties=prop)
plt.title('Training, Validation, and Test Accuracy', fontproperties=prop)
plt.grid(color='gray', linestyle='--', linewidth=0.5) 
plt.legend(prop=prop)

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()