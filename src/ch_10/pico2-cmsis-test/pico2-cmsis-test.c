//--------------------------------------------------------------------+
// CMSIS-DSP example for the Raspberry Pi Pico 2
//
// Copyright (c) 2026 David Such
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT
//--------------------------------------------------------------------+

#include <stdio.h>
#include <stdlib.h> // For rand()

#include "pico/stdlib.h"
#include "arm_math.h"

// FFT settings
#define FFT_SIZE  64  // Must be power of 2: 32, 64, 128, etc.

static float32_t input_signal[FFT_SIZE * 2];  // Real + Imaginary parts interleaved
static float32_t fft_output[FFT_SIZE];        // Magnitude results

int main() {
    stdio_init_all(); // Initialize UART for printf()

    // Wait for the USB to be connected
    while (!stdio_usb_connected()) {
        sleep_ms(100); // Sleep a bit to avoid busy-waiting
    }

    // Create a simple input signal: a single sine wave + noise
    for (int i = 0; i < FFT_SIZE; i++) {
        float32_t t = (float32_t)i / FFT_SIZE;
        // Real part: sine wave at frequency bin 5 + small random noise
        input_signal[2*i] = arm_sin_f32(2.0f * PI * 5.0f * t) + 0.2f * ((rand() % 100) / 100.0f - 0.5f);
        input_signal[2*i + 1] = 0.0f; // Imaginary part set to 0
    }

    // Create an instance of the CMSIS-DSP FFT
    arm_cfft_instance_f32 fft_inst;
    arm_cfft_init_f32(&fft_inst, FFT_SIZE);

    // Perform the complex FFT
    arm_cfft_f32(&fft_inst, input_signal, 0, 1);

    // Compute the magnitude of the complex numbers
    arm_cmplx_mag_f32(input_signal, fft_output, FFT_SIZE);

    // Output FFT results
    printf("FFT Magnitude Results:\n");
    for (int i = 0; i < FFT_SIZE / 2; i++) { // Only need to print half due to symmetry
        printf("Bin %2d: %0.3f\n", i, fft_output[i]);
    }

    // Loop forever
    while (true) {
        tight_loop_contents();
    }
}
