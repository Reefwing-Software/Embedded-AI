//--------------------------------------------------------------------+
// This example demonstrates how to use the PDM microphone driver on the
// Raspberry Pi Pico. It initializes the microphone, starts capturing audio
// samples, and prints them to the Serial Monitor. It is derived from the
// PDM microphone example provided in microphone-library-for-pico. The sample
// rate is set to 8 kHz, and the sample buffer size is set to 256 samples.
//
// The example uses the stdio_usb library for USB CDC communication.
//
// Note: Make sure to connect the PDM microphone to GPIO 2 (data) and GPIO 3 (clock).
// 
// Copyright (c) 2025 David Such
// 
// Original License:
// SPDX-FileCopyrightText: Copyright 2024 Arm Limited and/or its affiliates <open-source-office@arm.com>
// SPDX-License-Identifier: BSD-3-Clause
//--------------------------------------------------------------------+

 #include <stdio.h>
 #include <stdlib.h>        // For abs()
 
 #include "pico/stdlib.h"
 #include "pico/pdm_microphone.h"

 //--------------------------------------------------------------------+
 // DEFINITIONS
 //--------------------------------------------------------------------+
 #define SOUND_THRESHOLD 5000

 #ifdef CYW43_WL_GPIO_LED_PIN
// Pico W devices use a GPIO on the WIFI chip for the LED.
 #include "pico/cyw43_arch.h"
 #endif
 
 //---------------------------------------------------------------------+
 // CONFIGURATION
 //----------------------------------------------------------------------+
 const struct pdm_microphone_config config = {
     .gpio_data = 2,
     .gpio_clk = 3,
     .pio = pio0,
     .pio_sm = 0,
     .sample_rate = 8000,
     .sample_buffer_size = 256,
 };
 
 //---------------------------------------------------------------------+
 // VARIABLES
 //----------------------------------------------------------------------+
 int16_t sample_buffer[256];
 volatile int samples_read = 0;

 //---------------------------------------------------------------------+
 // PDM MICROPHONE HANDLER
 //----------------------------------------------------------------------+
 void on_pdm_samples_ready() {
     samples_read = pdm_microphone_read(sample_buffer, 256);
 }

 //--------------------------------------------------------------------+
 // LED CONTROL
 //--------------------------------------------------------------------+
 int pico_led_init(void) {
    #if defined(PICO_DEFAULT_LED_PIN)
        gpio_init(PICO_DEFAULT_LED_PIN);
        gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
        return PICO_OK;
    #elif defined(CYW43_WL_GPIO_LED_PIN)
        // For Pico W devices we need to initialise the driver etc
        return cyw43_arch_init();
    #endif
 }
        
 void pico_set_led(bool led_on) {
    #if defined(PICO_DEFAULT_LED_PIN)
        gpio_put(PICO_DEFAULT_LED_PIN, led_on);
    #elif defined(CYW43_WL_GPIO_LED_PIN)
        cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, led_on);
    #endif
 }

 //---------------------------------------------------------------------+
 // MAIN FUNCTION
 //----------------------------------------------------------------------+
 int main( void ) {
    stdio_usb_init();
    pico_led_init();
 
    // Wait for USB connection
    while (!stdio_usb_connected()) {
        tight_loop_contents();
    }
 
    printf("PDM Microphone Test\n");
 
    if (pdm_microphone_init(&config) < 0) {
         printf("PDM microphone initialization failed!\n");
         while (true) { tight_loop_contents(); }
    }
    printf("PDM microphone initialized\n");
    printf("Sample rate: %d Hz\n", config.sample_rate);
 
    pdm_microphone_set_samples_ready_handler(on_pdm_samples_ready);
 
    if (pdm_microphone_start() < 0) {
         printf("PDM microphone start failed!\n");
         while (true) { tight_loop_contents(); }
    }
    printf("PDM microphone started\n");
 
    while (true) {
         while (samples_read == 0) { tight_loop_contents(); }
 
         bool sound_detected = false;
         int sample_count = samples_read;
         samples_read = 0;
 
         for (int i = 0; i < sample_count; i++) {
            int16_t sample = sample_buffer[i];
            printf("%d\n", sample);
            if (abs(sample) > SOUND_THRESHOLD) {
                sound_detected = true;
            }
         }

         pico_set_led(sound_detected);
    }
 
    return 0;
 }
