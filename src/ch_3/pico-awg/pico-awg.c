// Copyright (c) 2025 David Such
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

#include <math.h>  // Required for sin() function

#include "pico/stdlib.h"
#include "pico/sync.h"
#include "hardware/sync.h"         // Required for __wfi()
#include "hardware/pio.h"          // Required for PIO functions
#include "hardware/clocks.h"       // Required for clock_get_hz()
#include "wavetable_output.pio.h"  // Generated PIO code

//--------------------------------------------------------------------+
// DEFINITIONS
//--------------------------------------------------------------------+

#define AWG_PIO pio0                // PIO instance to feed DAC
#define PIO_SM 0                    // PIO state machine number
#define PIO_PIN_BASE 8              // Start at GPIO8 to GPI15 (8 pins)

#define WAVE_TABLE_SIZE 256         // Number of samples in one full wave
#define PI 3.14159265358979323846

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

// Define the waveform buffer
uint8_t wave_table[WAVE_TABLE_SIZE] __attribute__((aligned(256)));

//--------------------------------------------------------------------+
// WAVE TABLE GENERATION FUNCTIONS
//--------------------------------------------------------------------+

// Function to generate a sine wave lookup table
void generate_sine_wave() {
    for (int i = 0; i < WAVE_TABLE_SIZE; ++i) {
        // Convert index to radians
        float angle = (float)i / WAVE_TABLE_SIZE * 2.0 * PI;  
        wave_table[i] = (uint8_t)(128 + (sin(angle) * 127));  // Scale to 0-255
    }
}

// Function to generate a triangle wave lookup table
void generate_triangle_wave() {
    int peak = WAVE_TABLE_SIZE / 2;  // Midpoint where the wave reaches max value

    for (int i = 0; i < WAVE_TABLE_SIZE; ++i) {
        if (i < peak) {
            // Rising phase (0 to 255)
            wave_table[i] = (uint8_t)(i * (255.0 / peak));  
        } else {
            // Falling phase (255 to 0)
            wave_table[i] = (uint8_t)((WAVE_TABLE_SIZE - i) * (255.0 / peak));  
        }
    }
}

// Function to generate a square wave with a variable duty cycle
void generate_square_wave(float duty_cycle) {
    if (duty_cycle < 0.0 || duty_cycle > 1.0) {
        duty_cycle = 0.5; // Default to 50% if out of range
    }

    int high_samples = (int)(WAVE_TABLE_SIZE * duty_cycle);  
    int low_samples = WAVE_TABLE_SIZE - high_samples;        

    for (int i = 0; i < WAVE_TABLE_SIZE; ++i) {
        if (i < high_samples) {
            wave_table[i] = 255;  // High state
        } else {
            wave_table[i] = 0;    // Low state
        }
    }
}

// Function to generate an amplitude modulated waveform
void generate_am_wave(float mod_index) {
    if (mod_index < 0.0 || mod_index > 1.0) {
        mod_index = 0.5;  // Default modulation index if out of range
    }

    for (int i = 0; i < WAVE_TABLE_SIZE; ++i) {
        float carrier_phase = (float)i / WAVE_TABLE_SIZE * 2.0 * PI;  
        float modulator_phase = (float)i / WAVE_TABLE_SIZE * PI;  
        
        // Amplitude varies from (1 - mod_index) to (1 + mod_index)
        float modulator = 1.0 + mod_index * sin(modulator_phase);  
        float carrier = sin(carrier_phase);  // Carrier wave

        float am_signal = modulator * carrier;  // Apply AM modulation

        // Scale to 0-255 range
        wave_table[i] = (uint8_t)(128 + (am_signal * 127));  
    }
}

//--------------------------------------------------------------------+
// PIO INITIALIZATION
//--------------------------------------------------------------------+
void pio_init(PIO pio, uint sm, uint offset, float freq) {
    float clk_div = clock_get_hz(clk_sys) / (4.0 * freq) ; 

    // Initialize GPIOs for PIO control
    for (uint j = PIO_PIN_BASE; j < (PIO_PIN_BASE + 8); j++) {
        pio_gpio_init(pio, j);  // Enable PIO output on each pin
    }

    // Configure PIO state machine settings
    pio_sm_config c = wavetable_output_program_get_default_config(offset);

    // Allocate out pin group to GPIO8–GPIO15 and set as output
    sm_config_set_out_pins(&c, PIO_PIN_BASE, 8);  
    pio_sm_set_consecutive_pindirs(pio, sm, PIO_PIN_BASE, 8, true);  

    // Set the PIO clock divider to achieve the desired frequency 
	sm_config_set_clkdiv(&c, clk_div);

    // Enable automatic pull after emptying TX FIFO, shift right.
    sm_config_set_out_shift(&c, true, true, 32);  

    // Initialize and enable the PIO state machine
    pio_sm_init(pio, sm, offset, &c);
    pio_sm_set_enabled(pio, sm, true);
}

//--------------------------------------------------------------------+
// PIO TX FIFO INTERRUPT HANDLER
//--------------------------------------------------------------------+

// Interrupt handler when TX FIFO is empty
void __isr pio_tx_empty_handler() {
    // Refill the TX FIFO (4 entries of 32-bit words)
    for (int j = 0; j < 4; j++) { 
        static int i = 0;  // Keep track of the waveform index

        uint32_t packed_data = (wave_table[i]     << 24) | 
                               (wave_table[i + 1] << 16) | 
                               (wave_table[i + 2] << 8)  | 
                               (wave_table[i + 3]);

        // Send packed data to TX FIFO
        pio_sm_put(AWG_PIO, PIO_SM, packed_data);

        // Increment waveform index (wrap around)
        i = (i + 4) % WAVE_TABLE_SIZE;
    }

    // Clear the interrupt flag
    pio_interrupt_clear(pio0, 0);
}

// Setup function to enable FIFO empty interrupt
void setup_pio_irq(PIO pio, uint sm) {
    pio_set_irq0_source_enabled(pio, PIO_INTR_SM0_TXNFULL_LSB, true);
    irq_set_exclusive_handler(PIO0_IRQ_0, pio_tx_empty_handler);
    irq_set_enabled(PIO0_IRQ_0, true);
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
// MAIN
//--------------------------------------------------------------------+

int main() {
    float freq = 100.0;  // Waveform frequency e.g., 100 Hz

    pico_led_init();

    // Load the PIO program into memory and initialize PIO
    uint offset = pio_add_program(AWG_PIO, &wavetable_output_program);

    pio_init(AWG_PIO, PIO_SM, offset, freq);    
    // generate_sine_wave(); // Generate a sine wave for testing
    generate_square_wave(0.5); // Generate a square wave for testing
    setup_pio_irq(AWG_PIO, PIO_SM); // Enable FIFO empty interrupt
    blink_interval_ms = BLINK_GENERATE;

    while (true) {
        __wfi();  // Enter low power mode until interrupt occurs
        led_blinking_task();
    }
}
