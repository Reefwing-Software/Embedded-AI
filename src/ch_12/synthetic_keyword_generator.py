# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import random
from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.generators import WhiteNoise

# Set the path to your Google Cloud service account JSON file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.expanduser(
    "~/Documents/GitHub/NSP-Embedded-AI/credentials/synthetic-keyword-generation.json"
)

# Set up the data folder
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_17/keyword")
os.makedirs(data_folder, exist_ok=True)

# Initialize Google Text-to-Speech client
client = texttospeech.TextToSpeechClient()

# Define parameters
text = "Hello World"
output_label = "helloworld"
num_samples = 1000  # Number of synthetic samples to generate
starting_number = 0  # Starting number for sample filenames

# Options for gender, language, and pitch
genders = [texttospeech.SsmlVoiceGender.MALE, texttospeech.SsmlVoiceGender.FEMALE, texttospeech.SsmlVoiceGender.NEUTRAL]
languages = ["en-US", "en-GB"]
pitch_range = (-5.0, 5.0)  # Range of pitch variation (in semitones)

for i in range(num_samples):
    # Generate random parameters
    rate = random.uniform(0.9, 1.1)  # Random speaking rate
    gender = random.choice(genders)
    language = random.choice(languages)
    pitch = random.uniform(*pitch_range)  # Random pitch within range

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code=language,
        ssml_gender=gender
    )

    # Configure the audio synthesis
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        speaking_rate=rate,
        pitch=pitch
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio to a file
    sample_number = starting_number + i + 1
    audio_path = os.path.join(data_folder, f"{output_label}_{sample_number}.wav")
    with open(audio_path, "wb") as out:
        out.write(response.audio_content)
    print(f"Generated {audio_path}")

    # Load the audio file
    audio = AudioSegment.from_wav(audio_path)

    # Generate white noise
    noise = WhiteNoise().to_audio_segment(duration=len(audio))

    # Set noise level (e.g., -20 dBFS)
    noise = noise - 20

    # Overlay noise onto the audio
    combined = audio.overlay(noise)

    # Export the combined audio with noise
    noisy_audio_path = os.path.join(data_folder, f"{output_label}_noisy_{sample_number}.wav")
    combined.export(noisy_audio_path, format="wav")
    print(f"Generated {noisy_audio_path}")