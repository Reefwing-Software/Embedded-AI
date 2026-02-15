// Copyright (c) 2025 David Such
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

#include <stdio.h>
#include <math.h>

#include "pico/stdlib.h"
#include "hardware/dma.h"
#include "hardware/irq.h"
#include "hardware/clocks.h"       
#include "wavetable_output.pio.h"  

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

// DMA channel number
static uint dmaData;

//--------------------------------------------------------------------+
// WAVE TABLE GENERATION FUNCTION
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

//--------------------------------------------------------------------+
// PIO INITIALIZATION
//--------------------------------------------------------------------+
float calculate_clk_div(float f_wave) {
    // Calculate the required PIO clock divider
    float f_sys = (float)clock_get_hz(clk_sys);
    float clk_div = f_sys / (f_wave * WAVE_TABLE_SIZE);

    // Check if the divider is within valid PIO limits
    if (clk_div < CLK_DIV_MIN) {
        printf("Warning: Desired frequency (%.2f Hz) is too high for %d samples.\n", f_wave, WAVE_TABLE_SIZE);
        blink_interval_ms = BLINK_ERROR; 
        return NAN;
    } else if (clk_div > CLK_DIV_MAX) {
        printf("Warning: Desired frequency (%.2f Hz) is too low.\n", f_wave);
        blink_interval_ms = BLINK_ERROR; 
        return NAN;
    }

    return clk_div;
}

void pio_init(PIO pio, uint sm, uint offset, float clk_div) { 
    for (uint j = PIO_PIN_BASE; j < (PIO_PIN_BASE + 8); j++) {
        pio_gpio_init(pio, j);  // Enable PIO output on each pin
    }

    pio_sm_config c = wavetable_output_program_get_default_config(offset);
    sm_config_set_out_pins(&c, PIO_PIN_BASE, 8);  
    pio_sm_set_consecutive_pindirs(pio, sm, PIO_PIN_BASE, 8, true);   
	sm_config_set_clkdiv(&c, clk_div);
    sm_config_set_out_shift(&c, true, true, 32);  
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
// DMA INTERRUPT HANDLER
//--------------------------------------------------------------------+
void dma_irq_handler() {
    // Clear the interrupt request
    dma_hw->ints0 = 1u << dmaData;

    // Restart the DMA channel
    dma_channel_set_read_addr(dmaData, &wave_table, true);
}

//--------------------------------------------------------------------+
// MAIN FUNCTION
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
        blink_interval_ms = BLINK_GENERATE; 

        // Initialize DMA channel
        dmaData = dma_claim_unused_channel(true);
        dma_channel_config c = dma_channel_get_default_config(dmaData);
        channel_config_set_transfer_data_size(&c, DMA_SIZE_32);
        channel_config_set_read_increment(&c, true);
        channel_config_set_dreq(&c, pio_get_dreq(AWG_PIO, PIO_SM, true));
        dma_channel_configure(
            dmaData, 
            &c, 
            &AWG_PIO->txf[PIO_SM], 
            NULL, 
            WAVE_TABLE_SIZE / 4, 
            false
        );

        // Tell the DMA to raise IRQ line 0 when the channel finishes a block
        dma_channel_set_irq0_enabled(dmaData, true);
        irq_set_exclusive_handler(DMA_IRQ_0, dma_irq_handler);
        irq_set_enabled(DMA_IRQ_0, true);
        dma_irq_handler();  // Start the DMA channel
    }

    while (true) {
        led_blinking_task();
    }
}
