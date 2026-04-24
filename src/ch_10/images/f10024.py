# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import requests
from scipy.io import wavfile
from scipy import signal

# Load custom font
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_10_v3")
image_name = 'f10024.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the local audio folder
audio_folder = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/data/ch_10')
os.makedirs(audio_folder, exist_ok=True)

# Download the audio sample
wave_file_name = "noisy_sample.wav"
wave_file_path = os.path.join(audio_folder, wave_file_name)

# Function to read and resample wave file
def read_wave_file(file, sample_rate):
    original_sample_rate, original_audio_data = wavfile.read(file)

    # Normalize input to float32 if needed
    if original_audio_data.dtype == np.float32:
        audio_data_float32 = original_audio_data
    else:
        audio_data_float32 = original_audio_data / np.iinfo(original_audio_data.dtype).max

    # Resample to target sample rate
    num_samples = int((len(audio_data_float32) / original_sample_rate) * sample_rate)
    audio_data = signal.resample(audio_data_float32, num_samples)

    return audio_data

# Parameters
audio_sample_rate = 16000  # Target resampled rate

# Read the audio file
audio_samples = read_wave_file(wave_file_path, audio_sample_rate)
print(f"Successfully read {len(audio_samples)} samples from '{wave_file_path}' with sample rate of {audio_sample_rate} Hz")

# Create a figure with two subplots
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot the waveform
ax1.plot(audio_samples, color='grey', linewidth=1)
ax1.set_title('Waveform', fontproperties=prop)
ax1.grid(True, linestyle='--', linewidth=0.5)
ax1.tick_params(axis='both', which='major', labelsize=10)
for label in (ax1.get_xticklabels() + ax1.get_yticklabels()):
    label.set_fontproperties(prop)

# Compute the spectrogram
f, t_spec, Sxx = signal.spectrogram(
    audio_samples, fs=audio_sample_rate, nperseg=256, noverlap=128
)

# dB scale
Sxx_log = 10 * np.log10(Sxx + 1e-10)

# Clip dynamic range
vmax = np.percentile(Sxx_log, 99)
vmin = vmax - 40            # was -60; narrower window = more contrast
Sxx_clipped = np.clip(Sxx_log, vmin, vmax)

# Normalise to 0..1
Sxx_norm = (Sxx_clipped - vmin) / (vmax - vmin)

# Gamma > 1 darkens the midtones (opposite direction from before, now
# that we are using cmap='gray' where 0 = black)
gamma = 2.0                 # was 0.6; try 1.5..2.5
Sxx_enhanced = Sxx_norm ** gamma

cax = ax2.pcolormesh(
    t_spec * audio_sample_rate, f, Sxx_enhanced,
    shading='auto', cmap='gray',
    vmin=0, vmax=1
)

# Colorbar needs to map back to dB for it to be meaningful
cbar = plt.colorbar(cax, ax=ax2, orientation='vertical')
cbar.set_label('Normalised intensity (dB, gamma-compressed)', fontproperties=prop)

# Original code for spectrogram plotting (commented out for now)
# Compute and plot the spectrogram
# f, t_spec, Sxx = signal.spectrogram(audio_samples, fs=audio_sample_rate, nperseg=256, noverlap=128)

# Plot spectrogram with greyscale
# cax = ax2.pcolormesh(t_spec * audio_sample_rate, f, Sxx, shading='gouraud', cmap='gray')

# Sxx_log = 10 * np.log10(Sxx + 1e-10)  # Apply log scaling for better contrast
# cax = ax2.pcolormesh(t_spec * audio_sample_rate, f, Sxx_log, shading='gouraud', cmap='gray')

# Add colorbar
# cbar = plt.colorbar(cax, ax=ax2, orientation='vertical')
# cbar.set_label('Intensity (dB)', fontproperties=prop)

# Style colorbar tick labels
cbar.ax.tick_params(labelsize=10)
for label in cbar.ax.get_yticklabels():
    label.set_fontproperties(prop)

ax2.set_ylabel('Frequency (Hz)', fontproperties=prop)
ax2.set_xlabel('Time (scrolling left to right)', fontproperties=prop)
ax2.set_title('Spectrogram', fontproperties=prop)
ax2.grid(True, linestyle='--', linewidth=0.5)
ax2.set_ylim(0, 8000)  # Up to 8 kHz for 16kHz sampled audio

ax2.tick_params(axis='both', which='major', labelsize=10)
for label in (ax2.get_xticklabels() + ax2.get_yticklabels()):
    label.set_fontproperties(prop)

# Save and show
plt.tight_layout()
plt.savefig(image_path, dpi=300, bbox_inches='tight')
plt.show()