// Copyright (c) 2025 David Such
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

#include <stdio.h>
#include <math.h>

#include "pico/stdlib.h"           // Required for Pico SDK functions
#include "hardware/dma.h"          // Required for DMA functions
#include "hardware/clocks.h"       // Required for clock_get_hz()
#include "wavetable_output.pio.h"  // Generated PIO code

//--------------------------------------------------------------------+
// DEFINITIONS
//--------------------------------------------------------------------+

#define AWG_PIO pio0                // PIO instance to feed DAC
#define PIO_SM 0                    // PIO state machine number
#define PIO_PIN_BASE 8              // Start at GPIO8 to GPI15 (8 pins)
#define CLK_DIV_MIN 1.0             // Define Min PIO clock divider
#define CLK_DIV_MAX 65535.0         // Max divider from RP2040 datasheet

#ifdef CYW43_WL_GPIO_LED_PIN
// Pico W devices use a GPIO on the WIFI chip for the LED.
#include "pico/cyw43_arch.h"
#endif

enum  {
    BLINK_ERROR = 250,
    BLINK_START = 1000,
    BLINK_GENERATE = 2500,
};

static uint32_t blink_interval_ms = BLINK_START;

#define WAVE_TABLE_SIZE 256  // Number of samples in one full wave
#define PI 3.14159265358979323846

// Define the waveform buffer
uint32_t wave_table[WAVE_TABLE_SIZE / 4] __attribute__((aligned(256)));

// DMA channel numbers
static uint dmaData;
static uint dmaCtrl;

//--------------------------------------------------------------------+
// WAVE TABLE GENERATION FUNCTIONS
//--------------------------------------------------------------------+

// Generate a sine wave lookup table - each 32-bit word stores 4 packed 8-bit values.
void generate_sine_wave() {
    for (int i = 0; i < WAVE_TABLE_SIZE / 4; ++i) {  // Process 4 samples at a time
        uint8_t sample1 = (uint8_t)(128 + (sin(((float)(i * 4)     / WAVE_TABLE_SIZE) * 2.0 * PI) * 127));
        uint8_t sample2 = (uint8_t)(128 + (sin(((float)(i * 4 + 1) / WAVE_TABLE_SIZE) * 2.0 * PI) * 127));
        uint8_t sample3 = (uint8_t)(128 + (sin(((float)(i * 4 + 2) / WAVE_TABLE_SIZE) * 2.0 * PI) * 127));
        uint8_t sample4 = (uint8_t)(128 + (sin(((float)(i * 4 + 3) / WAVE_TABLE_SIZE) * 2.0 * PI) * 127));

        wave_table[i] = (sample1 << 24) | (sample2 << 16) | (sample3 << 8) | sample4;
    }
}

// Function to generate a triangle wave lookup table
void generate_triangle_wave() {
    int peak = WAVE_TABLE_SIZE / 2;  // Midpoint where the wave reaches max value

    for (int i = 0; i < WAVE_TABLE_SIZE / 4; ++i) {  // Process 4 samples at a time
        uint8_t sample1, sample2, sample3, sample4;

        for (int j = 0; j < 4; j++) {
            int index = i * 4 + j;
            if (index < peak) {
                sample1 = (uint8_t)((float)index / peak * 255);  // Rising phase
            } else {
                sample1 = (uint8_t)((float)(WAVE_TABLE_SIZE - index) / peak * 255);  // Falling phase
            }

            if (j == 0) sample1 = sample1;
            if (j == 1) sample2 = sample1;
            if (j == 2) sample3 = sample1;
            if (j == 3) sample4 = sample1;
        }

        // Pack 4 samples into a 32-bit word
        wave_table[i] = (sample1 << 24) | (sample2 << 16) | (sample3 << 8) | sample4;
    }
}

// Function to generate a square wave with a variable duty cycle
void generate_square_wave(float duty_cycle) {
    if (duty_cycle < 0.0 || duty_cycle > 1.0) {
        duty_cycle = 0.5; // Default to 50% if out of range
    }

    int high_samples = (int)(WAVE_TABLE_SIZE * duty_cycle);  
    int low_samples = WAVE_TABLE_SIZE - high_samples;        

    for (int i = 0; i < WAVE_TABLE_SIZE / 4; ++i) {  // Process 4 samples at a time
        uint8_t sample1, sample2, sample3, sample4;

        for (int j = 0; j < 4; j++) {
            int index = i * 4 + j;
            if (index < high_samples) {
                sample1 = 255;  // High state
            } else {
                sample1 = 0;    // Low state
            }

            if (j == 0) sample1 = sample1;
            if (j == 1) sample2 = sample1;
            if (j == 2) sample3 = sample1;
            if (j == 3) sample4 = sample1;
        }

        // Pack 4 samples into a 32-bit word
        wave_table[i] = (sample1 << 24) | (sample2 << 16) | (sample3 << 8) | sample4;
    }
}

//--------------------------------------------------------------------+
// PIO INITIALIZATION
//--------------------------------------------------------------------+
float calculate_clk_div(float f_wave) {
    // Calculate the required PIO clock divider
    float f_sys = (float)clock_get_hz(clk_sys);
    float clk_div = f_sys / (f_wave * WAVE_TABLE_SIZE);

    // Check if the divider is within valid PIO limits
    if (clk_div < CLK_DIV_MIN || clk_div > CLK_DIV_MAX) {
        blink_interval_ms = BLINK_ERROR; 
        return NAN;
    }

    return clk_div;
}

void pio_init(PIO pio, uint sm, uint offset, float clk_div) {
    // Initialize GPIOs for PIO control
    for (uint j = PIO_PIN_BASE; j < (PIO_PIN_BASE + 8); j++) {
        pio_gpio_init(pio, j);  // Enable PIO output on each pin
    }

    pio_sm_config c = wavetable_output_program_get_default_config(offset);

    // Allocate out pin group to GPIO8–GPI15 and set as output
    sm_config_set_out_pins(&c, PIO_PIN_BASE, 8);  
    pio_sm_set_consecutive_pindirs(pio, sm, PIO_PIN_BASE, 8, true);  

    // Set the PIO clock divider to achieve the desired frequency 
	sm_config_set_clkdiv(&c, clk_div);

    // Enable automatic pull after emptying OSR, shift right.
    sm_config_set_out_shift(&c, true, true, 32);  

    // Initialize and enable the PIO state machine
    pio_sm_init(pio, sm, offset, &c);
    pio_sm_set_enabled(pio, sm, true);
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
      
static inline void pico_set_led(bool led_on) {
    #if defined(PICO_DEFAULT_LED_PIN)
        gpio_put(PICO_DEFAULT_LED_PIN, led_on);
    #elif defined(CYW43_WL_GPIO_LED_PIN)
        cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, led_on);
    #endif
}

void led_blinking_task(void) {
    static uint32_t start_ms = 0;
    static bool led_state = false;

    uint32_t current_time = to_ms_since_boot(get_absolute_time());

    if (current_time - start_ms < blink_interval_ms) return; // Not enough time
    start_ms = current_time; // Update last toggle time

    // Toggle LED state
    pico_set_led(led_state);
    led_state = !led_state;
}

//--------------------------------------------------------------------+
// DMA INITIALIZATION
//--------------------------------------------------------------------+

void dma_init(PIO pio, uint sm) {
    // Allocate two DMA channels:
    // - dmaData: Sends 32-bit data to the PIO state machine.
    // - dmaCtrl: Restarts dmaData when it completes.
    dmaData = dma_claim_unused_channel(true);
    dmaCtrl = dma_claim_unused_channel(true);

    // Configure the control DMA channel (dmaCtrl) to restart dmaData after completion
    dma_channel_config ctrlConfig = dma_channel_get_default_config(dmaCtrl);

    // Set transfer size to 32 bits (4 bytes per transfer)
    channel_config_set_transfer_data_size(&ctrlConfig, DMA_SIZE_32);

    // Disable read and write address incrementing since this channel only resets dmaData
    channel_config_set_read_increment(&ctrlConfig, false);
    channel_config_set_write_increment(&ctrlConfig, false);

    // Chain dmaCtrl to dmaData, when dmaCtrl finishes, it restarts dmaData
    channel_config_set_chain_to(&ctrlConfig, dmaData);

    // Disable IRQ generation to avoid unnecessary CPU overhead
    channel_config_set_irq_quiet(&ctrlConfig, true);

    // Set this channel to high priority to ensure continuous waveform playback
    channel_config_set_high_priority(&ctrlConfig, true);

    // Enable the control channel immediately
    channel_config_set_enable(&ctrlConfig, true);

    // Configure the dmaCtrl channel to reset dmaData's read address, allowing looping
    static uintptr_t wave_table_addr = (uintptr_t)wave_table; 

    dma_channel_configure(
        dmaCtrl, 
        &ctrlConfig,
        &dma_hw->ch[dmaData].read_addr, // Reset the read address of dmaData
        &wave_table_addr, // Reset to the start of the wave_table buffer
        1, // Transfer 1 word (32 bits) to reset the address
        false // Do not start yet
    );

    // ------------------------------------------------------------------------------------
    // Configure the data DMA channel (dmaData) to transfer waveform samples to PIO TX FIFO
    // ------------------------------------------------------------------------------------

    dma_channel_config dataConfig = dma_channel_get_default_config(dmaData);

    // Set transfer size to 32-bit words (4 bytes per transfer)
    channel_config_set_transfer_data_size(&dataConfig, DMA_SIZE_32);

    // Enable read address incrementing to step through the waveform buffer
    channel_config_set_read_increment(&dataConfig, true);

    // Disable write address incrementing, as all writes go to the same TX FIFO location
    channel_config_set_write_increment(&dataConfig, false);

    // Set DMA to be triggered by the PIO TX FIFO request (DREQ) when more data is needed
    channel_config_set_dreq(&dataConfig, pio_get_dreq(pio, sm, true));

    // Chain dmaData back to dmaCtrl so that after dmaData completes, dmaCtrl resets it
    channel_config_set_chain_to(&dataConfig, dmaCtrl);

    // Disable IRQ generation since we don’t need CPU involvement
    channel_config_set_irq_quiet(&dataConfig, true);

    // Set high priority to ensure continuous DMA transfer without stalling
    channel_config_set_high_priority(&dataConfig, true);

    // Enable the data channel
    channel_config_set_enable(&dataConfig, true);

    // Configure the dmaData channel to send waveform data to the PIO TX FIFO
    dma_channel_configure(
        dmaData,
        &dataConfig,
        &pio->txf[sm], // Write directly to the PIO TX FIFO
        wave_table, // Read from the wave_table buffer
        WAVE_TABLE_SIZE / 4, // Number of transfers, 32 bits at a time
        false // Do not start immediately
    );

    // Start the DMA channel
    dma_channel_start(dmaData);
}

//--------------------------------------------------------------------+
// MAIN
//--------------------------------------------------------------------+

int main()
{
    float freq = 488000.0;  // Waveform frequency in Hz
    float clk_div = calculate_clk_div(freq);

    pico_led_init();

    if (!isnan(clk_div)) {
        // Load the PIO program into memory and initialize PIO
        uint offset = pio_add_program(AWG_PIO, &wavetable_output_program);

        pio_init(AWG_PIO, PIO_SM, offset, clk_div);    
        generate_sine_wave(); 
        //generate_triangle_wave();
        blink_interval_ms = BLINK_GENERATE;

        dma_init(AWG_PIO, PIO_SM); // Initialize the DMA channels
    }

    while (true) {
        led_blinking_task();
    }
}
