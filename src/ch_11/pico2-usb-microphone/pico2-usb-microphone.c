//--------------------------------------------------------------------+
// This example demonstrates real-time audio noise suppression on the
// Raspberry Pi Pico 2. It initializes the microphone, starts capturing audio
// samples, denoises using RNNoise, and pushes a PCM USB audio stream using
// TinyUSB. It is derived from the USB PDM microphone example provided in 
// the Arm RNNoise examples for Pico 2 repository. The sample rate is set to
// 16 kHz, and the sample buffer size is set to 480 samples.
//
// The program has been modified to use the T3902 PDM microphone.
//
// Note: Make sure to connect the PDM microphone to GPIO 2 (data) and GPIO 3 (clock).
// 
// Copyright (c) 2025 David Such
// 
// Original License:
// SPDX-FileCopyrightText: Copyright 2024 Arm Limited and/or its affiliates <open-source-office@arm.com>
// SPDX-License-Identifier: BSD-3-Clause
//--------------------------------------------------------------------+

#include <pico/stdlib.h> 
#include <pico/multicore.h>
#include <hardware/gpio.h>
#include <hardware/pwm.h>

#include "pico/pdm_microphone.h"
#include "usb_microphone.h"
#include "rnnoise.h"

//--------------------------------------------------------------------+
// DEFINITIONS
//--------------------------------------------------------------------+
#define PDM_MICROPHONE_DATA_PIN 2
#define PDM_MICROPHONE_CLK_PIN 3
#define SUPPRESSION_ENABLED_PIN 15

#define PDM_MICROPHONE_PIO pio0
#define PDM_MICROPHONE_SM 0
#define PDM_MICROPHONE_SAMPLE_RATE 16000
#define PDM_MICROPHONE_BUFFER_SIZE 480

//---------------------------------------------------------------------+
// CONFIGURATION
//----------------------------------------------------------------------+
const struct pdm_microphone_config pdm_config = {
    .gpio_data = PDM_MICROPHONE_DATA_PIN,
    .gpio_clk = PDM_MICROPHONE_CLK_PIN,
    .pio = PDM_MICROPHONE_PIO,
    .pio_sm = PDM_MICROPHONE_SM,
    .sample_rate = PDM_MICROPHONE_SAMPLE_RATE,
    .sample_buffer_size = PDM_MICROPHONE_BUFFER_SIZE,
};

//---------------------------------------------------------------------+
// VARIABLES
//----------------------------------------------------------------------+
int16_t denoise_buffer[480];
uint16_t sample_buffer[480 * 2];
volatile bool new_samples = false;
volatile bool reset_indexes = false;
int in_index = 0;
int out_index = 0;
absolute_time_t last_tx = 0;

//---------------------------------------------------------------------+
// CALLBACK FUNCTIONS
//----------------------------------------------------------------------+
uint32_t core1_stack[0xc000 / sizeof(uint32_t)];

void on_pdm_samples_ready() {
  pdm_microphone_read(denoise_buffer, 480);
  new_samples = true;
}

void on_usb_microphone_tx_ready() {
  absolute_time_t now = get_absolute_time();

  if ((now - last_tx) > 2000) {
    reset_indexes = true;
  }
  last_tx = now;

  usb_microphone_write(&sample_buffer[out_index], 16 * 2);
  out_index = (out_index + 16) % (480 * 2);
}

void core1_entry() {
  gpio_set_function(PICO_DEFAULT_LED_PIN, GPIO_FUNC_PWM);
  uint slice_num = pwm_gpio_to_slice_num(PICO_DEFAULT_LED_PIN);
  pwm_config pwn_cfg = pwm_get_default_config();
  pwm_config_set_clkdiv(&pwn_cfg, 4.0f);
  pwm_init(slice_num, &pwn_cfg, true);

  float x_f32[480];
  DenoiseState* st = rnnoise_create(NULL);

  // run once to init
  memset(x_f32, 0x00, sizeof(x_f32));
  rnnoise_process_frame(st, x_f32, x_f32);

  // initialize and start the PDM microphone
  pdm_microphone_init(&pdm_config);
  pdm_microphone_set_samples_ready_handler(on_pdm_samples_ready);
  pdm_microphone_set_filter_gain(16);
  pdm_microphone_start();

  while (true) {
    while(!new_samples) {
      tight_loop_contents();
    }

    new_samples = false;

    if (reset_indexes) {
      out_index = 0;
      in_index = 480;
      reset_indexes = false;
    }
    
    float vad = 0.0;
    float* f32 = x_f32;
    int16_t* i16 = denoise_buffer;

    // copy new 16-bit samples to 32-bit floating point buffer
    for (int i = 0; i < 480; i++) {
      *f32++ = *i16++;
    }

    if (gpio_get(SUPPRESSION_ENABLED_PIN) == 0) {
      vad = rnnoise_process_frame(st, x_f32, x_f32);
    } else {
      // noise supression disabled
    }

    i16 = &sample_buffer[in_index];
    f32 = x_f32;

    // copy processed 32-bit floating point buffer to 16-bit with gain
    for (int i = 0; i < 480; i++) {
      *i16++ = *f32++;
    }

    in_index = (in_index + 480) % (480 * 2);
    pwm_set_gpio_level(PICO_DEFAULT_LED_PIN, (vad * 0xffff));
  }
}

//---------------------------------------------------------------------+
// MAIN FUNCTION
//----------------------------------------------------------------------+
int main(void) {
  stdio_init_all();

  // initialized GPIO pin for switch
  gpio_init(SUPPRESSION_ENABLED_PIN);
  gpio_pull_down(SUPPRESSION_ENABLED_PIN);
  gpio_set_dir(SUPPRESSION_ENABLED_PIN, GPIO_IN);

  // initialize the USB microphone interface
  usb_microphone_init();
  usb_microphone_set_tx_ready_handler(on_usb_microphone_tx_ready);

  multicore_launch_core1_with_stack(core1_entry, core1_stack, sizeof(core1_stack));

  while (true) {
    // run the USB microphone task continuously
    usb_microphone_task();
  }

  return 0;
}
