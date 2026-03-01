# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from keras.layers import TFSMLayer
from midi2audio import FluidSynth
from music21 import note, chord, instrument, stream, converter
from gan_training import load_notes, LATENT_DIM, OUTPUT_FOLDER

def create_midi(prediction_output, filename, instrument_type=instrument.Piano, offset_increment=0.5):
    """
    Convert the prediction output to a MIDI file.
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
    output_path = OUTPUT_FOLDER / f"{filename}.mid"
    midi_stream.write('midi', fp=str(output_path))
    print(f"MIDI file saved to: {output_path}")

    return str(output_path)

def generate_music(generator_model, latent_dim, n_vocab, length=100):
    """
    Generate new music using the trained generator model.
    """
    noise = np.random.normal(0, 1, (1, latent_dim))
    predictions = generator_model.predict(noise)
    
    # Flatten the predictions (from shape (1, 100, 1) to (100,))
    pred_array = predictions["output_0"] 
    pred_notes = pred_array.flatten()

    # Print the flattened array (100 notes)
    print("Generated notes:")
    print(pred_notes)

    # Scale predictions back to the original range of notes
    pred_notes_scaled = (pred_notes * (n_vocab / 2)) + (n_vocab / 2)

    # Map generated indices to note names
    pitchnames = sorted(set(item for item in notes))  
    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))
    pred_notes_mapped = [int_to_note[int(x)] for x in pred_notes_scaled[:length]]

    return pred_notes_mapped

def play_midi(midi_path):
    """
    Play the MIDI file using the fluidsynth library.
    """
    # Expand the full path for the soundfont
    soundfont_path = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/soundfonts/FluidR3_GM/FluidR3_GM.sf2")
    
    if not os.path.exists(soundfont_path):
        raise FileNotFoundError(f"SoundFont file not found at: {soundfont_path}")
    
    if not os.path.exists(midi_path):
        raise FileNotFoundError(f"MIDI file not found at: {midi_path}")
    
    # Use midi2audio's FluidSynth for MIDI playback
    fs = FluidSynth(soundfont_path)
    fs.play_midi(midi_path)

def visualize_midi(midi_path, prop, image_path):
    """
    Visualize a MIDI file as a piano roll using matplotlib.
    """

    # Ensure midi_path is a valid file
    if not midi_path.endswith(".mid"):
        raise ValueError(f"Invalid MIDI file: {midi_path} is not a .mid file.")

    # Parse the MIDI file
    midi_stream = converter.parse(midi_path)

    # Visualize the MIDI data
    plt.figure(figsize=(10, 6))
    for note_obj in midi_stream.flat.notes:
        if isinstance(note_obj, note.Note):
            plt.barh(note_obj.pitch.midi, note_obj.quarterLength, left=note_obj.offset, color="gray", edgecolor="black")

    plt.xlabel("Time (quarterLength)", fontproperties=prop)
    plt.ylabel("MIDI Note Number", fontproperties=prop)
    plt.title("Piano Roll", fontproperties=prop)

    # Save the plot
    plt.tight_layout()
    plt.savefig(image_path, dpi=300, bbox_inches="tight")
    plt.show()

if __name__ == '__main__':
    # Specify the font for plots
    font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
    prop = fm.FontProperties(fname=font_path, size=12)

    # Define the image folder and file name
    image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_5")
    image_name = 'f05025.pdf'
    image_path = os.path.join(image_folder, image_name)

    # Load the generator model
    generator_path = OUTPUT_FOLDER / "generator"
    generator = TFSMLayer(generator_path, call_endpoint="serving_default")
    generator_model = tf.keras.Sequential([generator])
    generator_model.summary()

    # Load processed notes
    saved_notes_file = OUTPUT_FOLDER / "extracted_notes.pkl"
    notes = load_notes(saved_notes_file)
    n_vocab = len(set(notes))

    # Generate new music
    generated_music = generate_music(generator_model, LATENT_DIM, n_vocab)

    # Create MIDI file
    midi_path = create_midi(generated_music, 'generated_music')

    # Play the MIDI file
    play_midi(midi_path)

    # Visualize the MIDI file
    visualize_midi(midi_path, prop, image_path)