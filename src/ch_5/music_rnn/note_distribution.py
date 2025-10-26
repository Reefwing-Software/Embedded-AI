# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import random
from pathlib import Path
import mido
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_5")
image_name = 'f05018.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = Path("~/Documents/GitHub/NSP-Embedded-AI/data/ch_5/maestro").expanduser()
extracted_folder = data_folder / "maestro-v3.0.0"
midi_files = list(extracted_folder.rglob("*.midi")) + list(extracted_folder.rglob("*.mid"))

# Select a random MIDI file
if not midi_files:
    raise FileNotFoundError("No MIDI files found in the dataset.")
random_midi_file = random.choice(midi_files)

# Parse the MIDI file and extract note data
def parse_midi(midi_file):
    mid = mido.MidiFile(midi_file)
    notes = []
    current_time = 0
    for msg in mid:
        current_time += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            notes.append({'start_time': current_time, 'pitch': msg.note, 'velocity': msg.velocity})
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            # Handle note_off or note_on with velocity=0
            for note in notes:
                if 'end_time' not in note and note['pitch'] == msg.note:
                    note['end_time'] = current_time
                    note['duration'] = current_time - note['start_time']
                    break
    return pd.DataFrame(notes)

# Generate note data
notes_df = parse_midi(random_midi_file)

# Add step column (time difference between note starts)
notes_df['step'] = notes_df['start_time'].diff().fillna(0)

# Plot distributions
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.hist(notes_df['pitch'], bins=20, color='gray', edgecolor='black')
plt.xlabel('Pitch', fontproperties=prop)
plt.ylabel('Count', fontproperties=prop)
plt.title('Pitch distribution', fontproperties=prop)
plt.grid(True, linestyle='--', alpha=0.5)

plt.subplot(1, 3, 2)
max_step = np.percentile(notes_df['step'], 97.5)  # Drop top 2.5% for cleaner visualization
plt.hist(notes_df['step'], bins=np.linspace(0, max_step, 21), color='gray', edgecolor='black')
plt.xlabel('Step (s)', fontproperties=prop)
plt.ylabel('Count', fontproperties=prop)
plt.title('Step distribution', fontproperties=prop)
plt.grid(True, linestyle='--', alpha=0.5)

plt.subplot(1, 3, 3)
max_duration = np.percentile(notes_df['duration'], 97.5)  # Drop top 2.5% for cleaner visualization
plt.hist(notes_df['duration'], bins=np.linspace(0, max_duration, 21), color='gray', edgecolor='black')
plt.xlabel('Duration (s)', fontproperties=prop)
plt.ylabel('Count', fontproperties=prop)
plt.title('Duration distribution', fontproperties=prop)
plt.grid(True, linestyle='--', alpha=0.5)

# Save and display the plot
os.makedirs(image_folder, exist_ok=True)
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()