# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import pickle
import tensorflow as tf
import numpy as np
import pandas as pd

from pathlib import Path
from sklearn.model_selection import train_test_split

# Define the data folder and dataset path
data_folder = Path("~/Documents/GitHub/NSP-Embedded-AI/data/ch_5/maestro").expanduser()
dataset_path = data_folder / "train_notes.tfrecord"
train_dataset_path = data_folder / "train_seq_ds_50.tfrecord" 
val_dataset_path = data_folder / "val_seq_ds_50.tfrecord" 
test_dataset_path = data_folder / "test_seq_ds_50.tfrecord"

# Load the dataset
notes_ds = tf.data.Dataset.load(str(dataset_path))

# Convert the dataset to a NumPy array for splitting
notes_array = np.array(list(notes_ds.as_numpy_iterator()))

# Split into training, validation, and testing sets
train_notes, temp_notes = train_test_split(notes_array, test_size=0.2, random_state=42)
val_notes, test_notes = train_test_split(temp_notes, test_size=0.5, random_state=42)

# Convert back to TensorFlow datasets
train_ds = tf.data.Dataset.from_tensor_slices(train_notes)
val_ds = tf.data.Dataset.from_tensor_slices(val_notes)
test_ds = tf.data.Dataset.from_tensor_slices(test_notes)

print(f"Training set size: {len(train_notes)}")
print(f"Validation set size: {len(val_notes)}")
print(f"Testing set size: {len(test_notes)}")

# Calculate scaling factors from the training data - use 95th percentile
train_notes_df = pd.DataFrame(train_notes, columns=['pitch', 'step', 'duration'])
duration_divider = np.percentile(train_notes_df['duration'], 95) 
step_divider = np.percentile(train_notes_df['step'], 95) 
pitch_min, pitch_max = train_notes_df['pitch'].min(), train_notes_df['pitch'].max()
step_min, step_max = train_notes_df['step'].min(), train_notes_df['step'].max()
duration_min, duration_max = train_notes_df['duration'].min(), train_notes_df['duration'].max()

# Save scaling factors using pickle
dividers_path = data_folder / "dividers.pkl"
with open(dividers_path, 'wb') as f:
    pickle.dump({'duration_divider': duration_divider, 
                 'step_divider': step_divider,
                 'pitch_min': pitch_min,
                 'pitch_max': pitch_max}, f)

def create_sequences(dataset: tf.data.Dataset, seq_length: int,
                     pitch_min = pitch_min, pitch_max = pitch_max,
                     step_min = step_min, step_max = step_max,
                     duration_min = duration_min, duration_max = duration_max) -> tf.data.Dataset:
    """Returns TF Dataset of sequence and label examples."""
    seq_length = seq_length + 1

    # Take 1 extra for the labels
    windows = dataset.window(seq_length, shift=1, stride=1, drop_remainder=True)

    # `flat_map` flattens the" dataset of datasets" into a dataset of tensors
    flatten = lambda x: x.batch(seq_length, drop_remainder=True)
    sequences = windows.flat_map(flatten)

    # Normalize note pitch, step, and duration
    def scale_features(x):
        x = tf.cast(x, tf.float32) # Cast to float for division
        x = tf.stack([(x[..., 0] - pitch_min) / (pitch_max - pitch_min),  # Pitch
                    (x[..., 1] - step_min) / (step_max - step_min),    # Step
                    (x[..., 2] - duration_min) / (duration_max - duration_min)], axis=-1) # Duration
        return x

    # Split the labels
    def split_labels(sequences):
        inputs = sequences[:-1]
        labels_dense = sequences[-1]
        labels = {key: labels_dense[i] for i, key in enumerate(['pitch', 'step', 'duration'])}
        return scale_features(inputs), labels

    return sequences.map(split_labels, num_parallel_calls=tf.data.AUTOTUNE).shuffle(1000)

# Parameters
seq_length = 50
batch_size = 32

# Create sequences for each split
train_seq_ds = create_sequences(train_ds, seq_length)
val_seq_ds = create_sequences(val_ds, seq_length)
test_seq_ds = create_sequences(test_ds, seq_length)

# Batch the datasets
train_seq_ds = (train_seq_ds
                .batch(batch_size, drop_remainder=True)
                .cache()
                .prefetch(tf.data.AUTOTUNE))

val_seq_ds = (val_seq_ds
              .batch(batch_size, drop_remainder=True)
              .cache()
              .prefetch(tf.data.AUTOTUNE))

test_seq_ds = (test_seq_ds
               .batch(batch_size, drop_remainder=True)
               .cache()
               .prefetch(tf.data.AUTOTUNE))

# Save datasets
train_seq_ds.save(str(train_dataset_path))
val_seq_ds.save(str(val_dataset_path))
test_seq_ds.save(str(test_dataset_path))

print(f"Training dataset saved to: {train_dataset_path}")
print(f"Validation dataset saved to: {val_dataset_path}")
print(f"Testing dataset saved to: {test_dataset_path}")