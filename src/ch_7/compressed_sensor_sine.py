# Copyright (c) 2024 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp

# Generate a sinusoidal signal
def generate_sinusoidal_signal(num_samples, frequency, amplitude, phase, noise_level=0.0):
    t = np.linspace(0, 1, num_samples, endpoint=False)
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    noise = noise_level * np.random.randn(num_samples)
    return signal + noise

# Create a Fourier-based measurement matrix
def create_fourier_measurement_matrix(num_samples, num_measurements):
    # Create a DFT (Discrete Fourier Transform) matrix
    dft_matrix = np.fft.fft(np.eye(num_samples)) / np.sqrt(num_samples)
    
    # Select random rows based on the provided number of measurements
    indices = np.random.choice(np.arange(num_samples), size=num_measurements, replace=False)
    measurement_matrix = dft_matrix[indices, :]
    
    return np.real(measurement_matrix), indices

# Reconstruct signal using L1 minimization with Fourier basis
def reconstruct_signal_fourier(num_samples, compressed_samples, measurement_matrix):
    # L1 minimization problem using CVXPY
    x = cp.Variable(num_samples, complex=True)  # Reconstructed signal in the Fourier domain
    objective = cp.Minimize(cp.norm1(x))  # L1 norm minimization
    
    # Constraints: Ensure the known measurements match
    constraints = [measurement_matrix @ x == compressed_samples]

    problem = cp.Problem(objective, constraints)
    problem.solve()
    
    # Inverse Fourier Transform to get the reconstructed time-domain signal
    reconstructed_signal = np.fft.ifft(x.value).real
    return reconstructed_signal

# Main function to generate, sample, and reconstruct the signal
def main():
    num_samples = 1000  # Total number of samples
    num_measurements = 100  # Number of compressed measurements
    frequency = 5  # Frequency of the sinusoid
    amplitude = 1  # Amplitude of the sinusoid
    phase = 0  # Phase shift
    noise_level = 0.1  # Optional noise level

    # Generate a sinusoidal signal
    original_signal = generate_sinusoidal_signal(num_samples, frequency, amplitude, phase, noise_level)

    # Create the Fourier measurement matrix and take compressed measurements
    measurement_matrix, indices = create_fourier_measurement_matrix(num_samples, num_measurements)
    compressed_samples = measurement_matrix @ original_signal  # Compressed measurements

    # Reconstruct the signal
    reconstructed_signal = reconstruct_signal_fourier(num_samples, compressed_samples, measurement_matrix)

    # Plot the original and reconstructed signals
    t = np.linspace(0, 1, num_samples, endpoint=False)
    plt.figure(figsize=(10, 6))
    plt.plot(t, original_signal, label='Original Signal', color='0.3')
    plt.plot(t, reconstructed_signal, label='Reconstructed Signal', linestyle='--', color='0.6')
    plt.title('Original vs Reconstructed Sinusoidal Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

# Run the example
if __name__ == "__main__":
    main()