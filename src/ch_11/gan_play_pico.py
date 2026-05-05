# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from pathlib import Path
from midi2audio import FluidSynth
from music21 import note, chord, instrument, stream, converter

# Input and output locations
INPUT_FOLDER = Path("~/Documents/GitHub/NSP-Embedded-AI/data/ch_11/GAN").expanduser()
IMAGE_FOLDER = Path("~/Documents/GitHub/NSP-Embedded-AI/images/ch_11_v5").expanduser()
OUTPUT_FOLDER = Path("~/Documents/GitHub/NSP-Embedded-AI/data/ch_4/GAN").expanduser()

# SoundFont file for MIDI playback
SOUNDFONT_PATH = Path("~/Documents/GitHub/NSP-Embedded-AI/soundfonts/FluidR3_GM/FluidR3_GM.sf2").expanduser()

# Load processed notes and determine vocabulary size
saved_notes_file = OUTPUT_FOLDER / "extracted_notes.pkl"
def load_notes(file_path):
    import pickle
    with open(file_path, "rb") as f:
        return pickle.load(f)

notes = load_notes(saved_notes_file)
n_vocab = len(set(notes))

# Create a mapping from index to note
pitchnames = sorted(set(item for item in notes))  
int_to_note = {number: note for number, note in enumerate(pitchnames)}

def dequantize_and_map_to_midi(int8_values):
    """
    Converts int8 model output values to MIDI note names.
    """
    # Convert int8 values to float32 using the output quantization parameters
    pred_notes = np.array(int8_values, dtype=np.float32) * 0.0078125  # Scale only (zero point = 0)

    # Scale predictions back to the original range of notes
    pred_notes_scaled = (pred_notes * (n_vocab / 2)) + (n_vocab / 2)

    # Convert to integers and ensure indices are within valid range
    pred_notes_mapped = [int_to_note[int(x)] for x in pred_notes_scaled]

    return pred_notes_mapped

def load_pico_output(file_path):
    """
    Reads int8 output values from a Pico inference text file and maps them to MIDI.
    """
    int8_values = []
    with open(file_path, "r") as f:
        for line in f:
            if "Output[" in line:  # Extract only int8 output lines
                value = int(line.split(":")[-1].strip().replace(",", ""))
                int8_values.append(value)
    
    return dequantize_and_map_to_midi(int8_values)

def create_midi(prediction_output, filename, instrument_type=instrument.Piano, offset_increment=0.5):
    """
    Converts a sequence of MIDI notes into a MIDI file.
    """
    offset = 0
    output_notes = []
    piano = instrument_type()

    for item in prediction_output:
        pattern = item[0]

        if ('.' in pattern) or pattern.isdigit():
            try:
                notes_in_chord = pattern.split('.')
                notes = [note.Note(int(n)) for n in notes_in_chord]
                for n in notes:
                    n.storedInstrument = piano
                new_chord = chord.Chord(notes)
                new_chord.offset = offset
                output_notes.append(new_chord)
            except ValueError:
                print(f"Skipping invalid chord pattern: {pattern}")

        else:
            try:
                new_note = note.Note(pattern)
                new_note.offset = offset
                new_note.storedInstrument = piano
                output_notes.append(new_note)
            except Exception as e:
                print(f"Skipping invalid note pattern: {pattern} ({e})")

        offset += offset_increment

    midi_stream = stream.Stream(output_notes)
    output_path = INPUT_FOLDER / f"{filename}.mid"
    midi_stream.write('midi', fp=str(output_path))
    print(f"MIDI file saved to: {output_path}")

    return str(output_path)

def play_midi(midi_path):
    """
    Plays the generated MIDI file using FluidSynth.
    """
    if not os.path.exists(SOUNDFONT_PATH):
        raise FileNotFoundError(f"SoundFont file not found at: {SOUNDFONT_PATH}")
    
    if not os.path.exists(midi_path):
        raise FileNotFoundError(f"MIDI file not found at: {midi_path}")
    
    # Use midi2audio's FluidSynth for MIDI playback
    fs = FluidSynth(str(SOUNDFONT_PATH))
    fs.play_midi(midi_path)

def visualize_midi(midi_path, prop, image_path):
    """
    Visualizes a MIDI file as a piano roll using matplotlib.
    """
    if not midi_path.endswith(".mid"):
        raise ValueError(f"Invalid MIDI file: {midi_path} is not a .mid file.")

    midi_stream = converter.parse(midi_path)

    plt.figure(figsize=(10, 6))
    for note_obj in midi_stream.flat.notes:
        if isinstance(note_obj, note.Note):
            plt.barh(note_obj.pitch.midi, note_obj.quarterLength, 
                     left=note_obj.offset, color="gray", edgecolor="black")

    plt.xlabel("Time (quarter length)", fontproperties=prop)
    plt.ylabel("MIDI note number", fontproperties=prop)
    plt.title("Piano roll", fontproperties=prop)

    plt.tight_layout()
    plt.savefig(image_path, dpi=300, bbox_inches="tight")
    plt.show()

if __name__ == '__main__':
    # Specify the font for plots
    font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
    prop = fm.FontProperties(fname=font_path, size=12)

    # Select an input file
    available_files = list(INPUT_FOLDER.glob("pico_inference_*.txt"))
    if not available_files:
        raise FileNotFoundError(f"No inference output files found in {INPUT_FOLDER}")

    print("\nAvailable Inference Files:")
    for idx, file in enumerate(available_files):
        print(f"{idx}: {file.name}")

    file_idx = int(input("\nSelect a file index to process: "))
    input_file = available_files[file_idx]

    # Load and process the Pico inference data
    print(f"Processing: {input_file.name}")
    midi_notes = load_pico_output(input_file)

    # Generate MIDI filename
    midi_filename = f"midi_from_pico_{file_idx}"

    # Create MIDI file
    midi_path = create_midi(midi_notes, midi_filename)

    # Play the MIDI file
    play_midi(midi_path)

    # Define and save the visualization
    image_name = f"midi_visualization_{file_idx}.pdf"
    image_path = IMAGE_FOLDER / image_name
    visualize_midi(midi_path, prop, image_path)