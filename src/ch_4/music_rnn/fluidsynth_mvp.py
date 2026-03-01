# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import fluidsynth
import time
import os

def test_fluidsynth(soundfont_path):
    soundfont_path = os.path.expanduser(soundfont_path)

    # Check if the SoundFont file exists
    if not os.path.isfile(soundfont_path):
        print(f"Error: SoundFont file not found at {soundfont_path}")
        return

    try:
        fs = fluidsynth.Synth()
        fs.start(driver="coreaudio")  # Set audio driver to 'coreaudio' (for macOS)
        sf_id = fs.sfload(soundfont_path) # Load the SoundFont
        fs.sample_rate = 44100.0  

    except Exception as e:
        print(f"Error initializing FluidSynth: {e}")
        return

    # Select a program (instrument) - 0 is usually Acoustic Grand Piano
    fs.program_select(0, sf_id, 0, 0)

    try:
        # Play a middle C note (MIDI note number 60) for 1 second
        print("Playing a C note...")
        fs.noteon(0, 60, 100)  # Channel 0, note 60, velocity 100
        time.sleep(1)
        fs.noteoff(0, 60)

        # Play a C major chord (notes 60, 64, 67) for 1 second
        print("Playing a C major chord...")
        fs.noteon(0, 60, 100)
        fs.noteon(0, 64, 100)
        fs.noteon(0, 67, 100)
        time.sleep(1)
        fs.noteoff(0, 60)
        fs.noteoff(0, 64)
        fs.noteoff(0, 67)

        print("Test complete. If you heard sound, FluidSynth is likely working.")

    except Exception as e:
        print(f"Error during playback: {e}")

    finally:
        # Clean up
        fs.delete()


if __name__ == "__main__":
    soundfont_path = "~/Documents/GitHub/NSP-Embedded-AI/soundfonts/FluidR3_GM/FluidR3_GM.sf2"
    test_fluidsynth(soundfont_path)