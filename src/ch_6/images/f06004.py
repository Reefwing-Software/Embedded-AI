# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# Specify the path to the .otf font file (update with your specific font path)
font_path = os.path.expanduser('~/Documents/GitHub/NSP-Embedded-AI/fonts/FuturaStd_forAUart/FuturaStd-Book.otf')
prop = fm.FontProperties(fname=font_path, size=12)

# Define the image folder and file name
image_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/images/ch_6_v5")
image_name = 'f06004.pdf'
image_path = os.path.join(image_folder, image_name)

# Define the data folder and file name
data_folder = os.path.expanduser("~/Documents/GitHub/NSP-Embedded-AI/data/ch_6")
file_name = "compressed_sensor_data.txt"
file_path = os.path.join(data_folder, file_name)

# Function to read sensor data from a text file
def read_arduino_output(filename):
    regular_samples = []
    compressed_samples = {}
    reading_compressed = False
    reading_regular = False

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            
            # Ignore empty lines or lines that don't contain 'Sample'
            if not line or "Sample" not in line:
                continue

            if "Compressed Samples" in line:
                reading_compressed = True
                reading_regular = False
                continue
            elif "All Regular Samples" in line:
                reading_regular = True
                reading_compressed = False
                continue

            # Safely split and handle potential errors
            try:
                parts = line.split(":")
                index = int(parts[0].split()[1])  # Extract index (e.g., "Sample 7:")
                value = float(parts[1].strip().split()[0])  # Extract temperature value (e.g., "23 °C")

                if reading_compressed:
                    compressed_samples[index] = value
                elif reading_regular:
                    regular_samples.append(value)

            except (IndexError, ValueError) as e:
                # Print or log any problematic lines for debugging
                print(f"Error processing line: {line}, Error: {e}")
    
    return regular_samples, compressed_samples

# FFT and Plotting function
def plot_fft(temperature_samples, fs=0.00167):
    num_samples = len(temperature_samples)

    # Perform FFT
    fft_result = np.fft.fft(temperature_samples)
    frequencies = np.fft.fftfreq(num_samples, d=1/fs)

    # Calculate the magnitude of the FFT result
    magnitude = np.abs(fft_result)

    # Create the figure
    plt.figure(figsize=(10, 6))

    # Plot the frequency components in grayscale
    plt.stem(frequencies, magnitude, linefmt='0.4', markerfmt='o', basefmt='0.2')  # Dark gray stems, markers
    plt.title('Frequency domain representation (sparsity)', fontproperties=prop)
    plt.xlabel('Frequency (Hz)', fontproperties=prop)
    plt.ylabel('Magnitude', fontproperties=prop)

    # Apply the custom font to the grid and other elements
    plt.grid(True, color='0.8')  # Light gray grid

    # Show plot
    plt.tight_layout()
    plt.savefig(image_path, dpi=300, bbox_inches='tight')
    plt.show()

# Main function
if __name__ == '__main__':
    # Assign Arduino sensor data from file
    regular_samples, compressed_samples = read_arduino_output(file_path)

    # Check extracted data
    num_samples = len(regular_samples)
    num_compressed = len(compressed_samples)
    print("Samples Extracted: ", num_samples)
    print("Compressed Samples: ", num_compressed)
    
    # Plot sample in the frequency domain - Discrete Fourier Transform (DFT)
    plot_fft(regular_samples)