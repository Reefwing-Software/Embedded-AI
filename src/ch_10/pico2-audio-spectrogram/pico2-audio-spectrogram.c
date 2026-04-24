//--------------------------------------------------------------------+
// pico2-audio-spectrogram.c
//
// This program displays an audio spectrogram of PDM microphone samples 
// with and without RNN noise suppression. The PDM microphone is connected 
// to GPIO 2 (data) and GPIO 3 (clock).
//
// Copyright (c) 2026 David Such
//
// Attributions:
//  - Some code is derived from the ARM RNNoise & spectrogram examples for the Pico. 
//    SPDX-License-Identifier: Apache-2.0
//  - Libraries used (see included LICENSE files):
//    - microphone-library-for pico
//    - OpenPDM2PCM
//    - RNNoise
//    - CMSIS_6 and CMSIS_DSP
//    - reefwing-st7789
//
// This software is released under the MIT License.
//
//--------------------------------------------------------------------+

#include <stdio.h>
#include <pico/stdlib.h> 
#include <pico/multicore.h>
#include <hardware/gpio.h>
#include <hardware/pwm.h>

#include "pico/pdm_microphone.h"
#include "usb_microphone.h"
#include "rnnoise.h"
#include "arm_math.h"
#include "reefwing_st7789.h"
#include "reefwing_rgb565_colors.h"
#include "spectrogram_colormap.h"

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

#define LCD_PIO pio1
#define LCD_SM 0
#define LCD_WIDTH   SCREEN_WIDTH
#define LCD_HEIGHT  SCREEN_HEIGHT

#define FFT_SIZE            256
#define INPUT_BUFFER_SIZE   64
#define INPUT_SHIFT         2
#define FFT_BINS_SKIP       5
#define FFT_MAG_MAX         2000.0f

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

reefwing_st7789_config_t lcd_config = {
    .pin_bl = 17,
    .pin_dc = 18,
    .pin_rst = 19,
    .pin_cs = 20,
    .pin_din = 26,
    .pin_clk = 27,
    .spi_polarity = true,
    .clk_div = 2.0f
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

q15_t capture_buffer_q15[INPUT_BUFFER_SIZE];
volatile int new_samples_captured = 0;

q15_t input_q15[FFT_SIZE];
q15_t window_q15[FFT_SIZE];
q15_t windowed_input_q15[FFT_SIZE];
q15_t fft_q15[FFT_SIZE * 2];
q15_t fft_mag_q15[FFT_SIZE / 2];
uint16_t row_pixels[LCD_WIDTH];

arm_rfft_instance_q15 S_q15;
uint16_t row = 0;

//---------------------------------------------------------------------+
// CALLBACK FUNCTIONS
//----------------------------------------------------------------------+
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

//---------------------------------------------------------------------+
// FFT HANNING WINDOW
//---------------------------------------------------------------------+
void hanning_window_init_q15(q15_t* window, size_t size) {
    for (size_t i = 0; i < size; i++) {
      float32_t f = 0.5f * (1.0f - arm_cos_f32(2 * PI * i / FFT_SIZE));
      arm_float_to_q15(&f, &window[i], 1);
    }
}
  
//---------------------------------------------------------------------+
// CORE 1 MAIN ENTRY
//---------------------------------------------------------------------+
uint32_t core1_stack[0xc000 / sizeof(uint32_t)];

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

  // initialize the LCD display
  reefwing_st7789_init(LCD_PIO, LCD_SM, &lcd_config);
  reefwing_st7789_fill_screen(ST_BLACK);

  // initialize the FFT
  hanning_window_init_q15(window_q15, FFT_SIZE);
  arm_rfft_init_q15(&S_q15, FFT_SIZE, 0, 1);

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
    } 

    i16 = &sample_buffer[in_index];
    f32 = x_f32;

    // copy processed 32-bit floating point buffer to 16-bit with gain
    for (int i = 0; i < 480; i++) {
      *i16++ = *f32++;
    }

    in_index = (in_index + 480) % (480 * 2);
    pwm_set_gpio_level(PICO_DEFAULT_LED_PIN, (vad * 0xffff));

    // ------------- Spectrogram Drawing --------------- //
    // Move input buffer values over
    arm_copy_q15(input_q15 + INPUT_BUFFER_SIZE, input_q15, FFT_SIZE - INPUT_BUFFER_SIZE);

    // Shift and copy in new samples
    for (int i = 0; i < INPUT_BUFFER_SIZE; i++) {
      capture_buffer_q15[i] = (q15_t)(denoise_buffer[i] << INPUT_SHIFT);
    }
    arm_copy_q15(capture_buffer_q15, input_q15 + (FFT_SIZE - INPUT_BUFFER_SIZE), INPUT_BUFFER_SIZE);

    arm_mult_q15(window_q15, input_q15, windowed_input_q15, FFT_SIZE);
    arm_rfft_q15(&S_q15, windowed_input_q15, fft_q15);
    arm_cmplx_mag_q15(fft_q15, fft_mag_q15, FFT_SIZE / 2);

    for (int i = 0; i < (LCD_WIDTH / 2); i++) {
      q15_t magnitude = fft_mag_q15[i + FFT_BINS_SKIP];

      int color_index = (magnitude / FFT_MAG_MAX) * 255;
      if (color_index > 255) color_index = 255;
      if (color_index < 0) color_index = 0;

      uint16_t pixel = SPECTROGRAM_COLOR_MAP[color_index];
      row_pixels[LCD_WIDTH - 1 - (i * 2)] = pixel;
      row_pixels[LCD_WIDTH - 1 - (i * 2 + 1)] = pixel;
    }

    reefwing_st7789_set_cursor(0, row);
    reefwing_st7789_set_window(0, row, LCD_WIDTH - 1, row);
    reefwing_st7789_start_pixels();

    // Write the entire row pixel-by-pixel
    for (int i = 0; i < LCD_WIDTH; i++) {
        reefwing_st7789_put(row_pixels[i]);
    }
    reefwing_st7789_vertical_scroll(row);

    row = (row + 1) % LCD_HEIGHT;
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
      usb_microphone_task();
    }
  
    return 0;
  }
