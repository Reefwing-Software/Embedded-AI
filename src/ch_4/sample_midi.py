# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import fluidsynth
import time
import os
import random
import mido
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from pathlib import Path

def note_number_to_name(note_number):
    """Converts a MIDI note number to its name (e.g., 60 -> 'C4')."""
    if not 0 <= note_number <= 127:
        return "Invalid Note"

    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = note_number // 12 - 1
    note_name = notes[note_number % 12]
    return f"{note_name}{octave}"

def play_and_visualize_midi(midi_file, duration=15):  
    """
    Plays a MIDI file using FluidSynth (up to a specified duration) and visualizes 
    the MIDI data using Matplotlib.

    Args:
        midi_file: Path to the MIDI file.
        duration: Duration of playback in seconds (default: 15).
    """

    # --- Play MIDI with FluidSynth ---
    try:
        fs = fluidsynth.Synth()
        fs.start(driver="coreaudio")
        fs.sample_rate = 16000.0

        sf_path = "~/Documents/GitHub/NSP-Embedded-AI/soundfonts/FluidR3_GM/FluidR3_GM.sf2"
        sf_id = fs.sfload(os.path.expanduser(sf_path))
        fs.program_select(0, sf_id, 0, 0)

        midi_file_name = Path(midi_file).name  # Extract filename from path
        print(f"Playing MIDI file: {midi_file_name} (up to {duration} seconds)")

        mid = mido.MidiFile(midi_file)
        start_time = time.time()
        for msg in mid.play():
            if time.time() - start_time >= duration:
                print("Stopping playback after", duration, "seconds.")
                break

            if msg.type == 'note_on' or msg.type == 'note_off':
                fs.noteon(msg.channel, msg.note, msg.velocity)
            time.sleep(msg.time)

    except Exception as e:
        print(f"Error playing MIDI: {e}")
        return
    finally:
        fs.delete()

    # --- Visualize MIDI as Piano Roll ---
    try:
        mid = mido.MidiFile(midi_file)

        # Store note events as (start_time, end_time, note, velocity)
        note_events = []
        current_notes = {}
        current_time = 0

        for msg in mid:
            current_time += msg.time

            if msg.type == 'note_on' and msg.velocity > 0:  # Handle note_on with velocity > 0
                current_notes[msg.note] = (current_time, msg.velocity)
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):  # Treat note_on with velocity 0 as note_off
                if msg.note in current_notes:
                    start_time, velocity = current_notes.pop(msg.note)
                    note_events.append((start_time, current_time, msg.note, velocity))

        # Create a Pandas DataFrame and limit to the first 20 notes
        notes_df = pd.DataFrame(note_events, columns=['start', 'end', 'pitch', 'velocity']).head(20)

        # --- Plotting with matplotlib ---
        plt.figure(figsize=(12, 6))

        # Plot horizontal bars for each note
        for index, row in notes_df.iterrows():
            plt.barh(row['pitch'], width=row['end'] - row['start'], left=row['start'], color='gray', edgecolor='black')

        plt.xlabel('Time (s)', fontproperties=prop)
        plt.ylabel('MIDI note number', fontproperties=prop)
        plt.title(f'Piano roll (first 20 notes): {midi_file_name}', fontproperties=prop)
        plt.xticks(fontproperties=prop)
        plt.yticks(fontproperties=prop)

        # Set y-ticks to note names
        min_note = int(notes_df['pitch'].min())
        max_note = int(notes_df['pitch'].max())
        note_names = [note_number_to_name(n) for n in range(min_note, max_note + 1)]
        plt.yticks(range(min_note, max_note + 1), note_names)

        # Show the plot
        plt.tight_layout()
        plt.savefig(image_path, dpi=300, bbox_inches='tight')
        plt.show()

    except Exception as e:
        print(f"Error visualizing MIDI: {e}")


# --- Main Script ---

# Specify the path to the .otf font file
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_5")
image_name = 'f05017d.pdf'
image_path = os.path.join(image_folder, image_name)

# Create the directory if it doesn't exist
os.makedirs(image_folder, exist_ok=True)

data_folder = Path("~/Documents/GitHub/NSP-Embedded-AI/data/ch_5/maestro").expanduser()
extracted_folder = data_folder / "maestro-v3.0.0"
midi_files = list(extracted_folder.rglob("*.midi")) + list(extracted_folder.rglob("*.mid"))

if not midi_files:
    print("No MIDI files found in the specified directory.")
else:
    random_midi_file = random.choice(midi_files)
    play_and_visualize_midi(random_midi_file)