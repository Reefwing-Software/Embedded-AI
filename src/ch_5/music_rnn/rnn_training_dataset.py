# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import random
import numpy as np
import tensorflow as tf
import pandas as pd
from pathlib import Path
import mido

# Define the data folder and file name
data_folder = Path("~/Documents/GitHub/NSP-Embedded-AI/data/ch_5/maestro").expanduser()
extracted_folder = data_folder / "maestro-v3.0.0"
midi_files = list(extracted_folder.rglob("*.midi")) + list(extracted_folder.rglob("*.mid"))

def midi_to_notes(midi_file: str) -> pd.DataFrame:
    """Extracts notes from a MIDI file and returns a DataFrame."""
    mid = mido.MidiFile(midi_file)
    notes = {'pitch': [], 'start': [], 'end': [], 'step': [], 'duration': [], 'velocity': []}

    current_time = 0
    previous_note_end = 0
    active_notes = {}  # Tracks currently active notes

    for msg in mid:
        current_time += msg.time

        if msg.type == 'note_on' and msg.velocity > 0:
            # Start a new note 
            active_notes[msg.note] = (current_time, msg.velocity) 

        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            # End the note if it's active
            if msg.note in active_notes:
                start_time, velocity = active_notes.pop(msg.note)
                notes['pitch'].append(msg.note)
                notes['start'].append(start_time)
                notes['end'].append(current_time)
                notes['step'].append(current_time - previous_note_end) 
                notes['duration'].append(current_time - start_time)
                notes['velocity'].append(velocity) 

                previous_note_end = current_time

    # Ensure all lists are of equal length and create the DataFrame
    if not notes['pitch']:  # Handle case with no valid notes
        print(f"No valid notes found in {midi_file}")
        return pd.DataFrame(columns=['pitch', 'start', 'end', 'step', 'duration'])

    return pd.DataFrame({name: np.array(value) for name, value in notes.items()})

# Option to parse all MIDI files or a sample
parse_all = True  # Set to True to parse all MIDI files
num_files_to_sample = 100  # Number of files to sample if parse_all is False

if parse_all:
    sampled_files = midi_files
else:
    sampled_files = random.sample(midi_files, min(num_files_to_sample, len(midi_files)))

# Parse notes from the sampled MIDI files
all_notes = {'pitch': [], 'step': [], 'duration': []}
for midi_file in sampled_files:
    notes = midi_to_notes(str(midi_file))
    for key in all_notes:
        all_notes[key].extend(notes[key])

# Print the total number of notes parsed
print(f"Number of notes parsed: {len(all_notes['pitch'])}")

# Create a TensorFlow dataset
key_order = ['pitch', 'step', 'duration']
train_notes = np.stack([all_notes[key] for key in key_order], axis=1)
notes_ds = tf.data.Dataset.from_tensor_slices(train_notes)

# Save the dataset to the data folder
dataset_path = data_folder / "train_notes.tfrecord"
notes_ds.save(str(dataset_path))
print(f"Dataset saved to: {dataset_path}")

# Print out a sample of the dataset
print("Sample of the dataset:")
for sample in notes_ds.take(5):
    print(sample.numpy())