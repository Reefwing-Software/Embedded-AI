// Copyright (c) 2026 David Such
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

#include <stdio.h>

#include "pico/stdlib.h"
#include "touch.pio.h"
#include "hardware/uart.h"

#define TOUCH_PIO pio0         // PIO instance for touch sensing
#define TOUCH_PIN 2            // GPIO number for the first touch button
#define TOUCH_NUMBER 15        // Number of sequential touch buttons
#define TOUCH_SM_COUNT ((TOUCH_NUMBER + 4) / 5)  // State machines required
#define CLOCK_DIV 50           // Clock divider for PIO - tune for sensitivity
#define DRIVE_STRENGTH 4       // Drive strength: 2mA, 4mA, 8mA, or 12mA
#define FAST_SLEW false        // Slew rate: true (fast), false (slow)

#define MIDI_UART uart0
#define MIDI_TX_PIN 0          // GPIO0 = UART0 TX
#define MIDI_BAUD_RATE 31250

#define MIDI_CHANNEL 0         // Channel 1 (0–15)
#define MIDI_NOTE_ON  (0x90 | MIDI_CHANNEL)
#define MIDI_NOTE_OFF (0x80 | MIDI_CHANNEL)

#define BASE_NOTE 60            // Middle C
#define DEFAULT_VELOCITY 100
#define OCTAVE_STEP 12          // Semitones per octave
#define OCTAVE_MIN -3
#define OCTAVE_MAX 3

// Output mode selection
#define OUTPUT_SERIAL 0
#define OUTPUT_MIDI   1

#define OUTPUT_MODE OUTPUT_SERIAL  // Change to OUTPUT_SERIAL as needed

// Key labels corresponding to the 15 touch buttons
const char *key_labels[TOUCH_NUMBER] = {
    "C", "C#", "D", "D#", "E", "F", 
    "F#", "G", "G#", "A", "A#", "B", 
    "Octave +", "Octave -", "AI"
};

// Pico W devices use a GPIO on the WIFI chip for the LED.
#ifdef CYW43_WL_GPIO_LED_PIN
#include "pico/cyw43_arch.h"
#endif

// Perform initialisation
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

void wait_for_usb_serial() {
    while (!stdio_usb_connected()) {
        sleep_ms(10);  // Wait for USB serial connection
    }
}

// ISR-shared state; keep file-local to avoid accidental external access.
static volatile uint touch_state = 0;
static volatile uint touch_state_last = 0;
static volatile bool touch_change_flg = false;

// Interrupt handler for touch detection
void touch_isr_handler(void) {
    for (int sm = 0; sm < TOUCH_SM_COUNT; sm++) {
        if (!pio_sm_is_rx_fifo_empty(TOUCH_PIO, sm)) {
            uint shift = sm * 5;  // Dynamically calculate shift for each state machine
            touch_state = (touch_state & ~(0x1F << shift)) | (pio_sm_get(TOUCH_PIO, sm) << shift);
        }
    }

    if (touch_state != touch_state_last) {
        touch_change_flg = true;
        touch_state_last = touch_state;
    }
}

// Initialize touch sensing
int touch_setup(PIO pio_touch, int num_buttons, int start_pin, float clk_div, uint drive_strength, bool fast_slew) {
    
    int sm;
    uint offset_touch = pio_add_program(TOUCH_PIO, &touch_program);
    
    for (int i = 0; i < TOUCH_SM_COUNT; i++) {
        sm = pio_claim_unused_sm(pio_touch, true);

        if (sm < 0) {  
            printf("Error: No available state machines\n");
            return 1;  
        }
        
        pio_set_irq0_source_enabled(pio_touch, sm, true);
        touch_init(pio_touch, sm, offset_touch, start_pin + (i * 5), 5, clk_div, drive_strength, fast_slew);
        pio_sm_set_enabled(pio_touch, sm, true);
    }

    irq_set_exclusive_handler(PIO0_IRQ_0, touch_isr_handler);
    irq_set_enabled(PIO0_IRQ_0, true);
    
    return 0;
}

static inline void midi_note_on(uint8_t note, uint8_t velocity) {
    uart_putc_raw(MIDI_UART, MIDI_NOTE_ON);
    uart_putc_raw(MIDI_UART, note);
    uart_putc_raw(MIDI_UART, velocity);
}

static inline void midi_note_off(uint8_t note) {
    uart_putc_raw(MIDI_UART, MIDI_NOTE_OFF);
    uart_putc_raw(MIDI_UART, note);
    uart_putc_raw(MIDI_UART, 0x00);
}

static int octave_offset = 0;   // Octave offset in semitones

static inline void key_pressed(uint8_t key) {
#if OUTPUT_MODE == OUTPUT_SERIAL
    printf("Key Pressed: %s\n", key_labels[key]);
#elif OUTPUT_MODE == OUTPUT_MIDI
    if (key == 12) {
        if (octave_offset < (OCTAVE_MAX * OCTAVE_STEP)) {
            octave_offset += OCTAVE_STEP;
        }
    } else if (key == 13) {
        if (octave_offset > (OCTAVE_MIN * OCTAVE_STEP)) {
            octave_offset -= OCTAVE_STEP;
        }
    } else if (key < 12) {
        midi_note_on(BASE_NOTE + key + octave_offset, DEFAULT_VELOCITY);
    }
#endif
}

static inline void key_released(uint8_t key) {
#if OUTPUT_MODE == OUTPUT_SERIAL
    printf("Key Released: %s\n", key_labels[key]);
#elif OUTPUT_MODE == OUTPUT_MIDI
    if (key < 12) {
        midi_note_off(BASE_NOTE + key + octave_offset);
    }
#endif
}

int main()
{
    stdio_init_all();
    pico_led_init();

    // Initialise UART for MIDI
    uart_init(MIDI_UART, MIDI_BAUD_RATE);
    gpio_set_function(MIDI_TX_PIN, GPIO_FUNC_UART);
    uart_set_format(MIDI_UART, 8, 1, UART_PARITY_NONE);
    uart_set_fifo_enabled(MIDI_UART, false);

    if (OUTPUT_MODE == OUTPUT_SERIAL) {
        wait_for_usb_serial();
    }

    printf("Pico Keyboard version 2.0\n");
    printf("Initializing touch keys...\n");
    if (touch_setup(TOUCH_PIO, TOUCH_NUMBER, TOUCH_PIN, CLOCK_DIV, DRIVE_STRENGTH, FAST_SLEW) != 0) {
        printf("Touch setup failed; halting.\n");
        while (true) {
            tight_loop_contents();
        }
    }

    uint key_active_state = 0;  // Track which keys are currently pressed

    while (true) {
        if (touch_change_flg) {
            // Prevent ISR from updating while we snapshot state.
            irq_set_enabled(PIO0_IRQ_0, false);
            uint local_touch_state = touch_state;
            touch_change_flg = false;
            irq_set_enabled(PIO0_IRQ_0, true);

            // If new keys are pressed, assume all other keys were released
            uint new_keys_pressed = local_touch_state & ~key_active_state;  // Newly pressed keys
            uint keys_released = key_active_state & ~local_touch_state;     // Keys that were released

            // If any new key is pressed, all other keys are considered released
            if (new_keys_pressed) {
                keys_released = key_active_state & ~new_keys_pressed;
            }

            // Update the active key state
            key_active_state = local_touch_state;

            // Print newly pressed keys
            if (new_keys_pressed) {
                for (int i = 0; i < TOUCH_NUMBER; i++) {
                    if (new_keys_pressed & (1 << i)) {
                        key_pressed(i);
                    }
                }

                // Turn on LED if at least one key is pressed
                pico_set_led(true);
            }

            // Print released keys
            if (keys_released) {
                for (int i = 0; i < TOUCH_NUMBER; i++) {
                    if (keys_released & (1 << i)) {
                        key_released(i);
                    }
                }
            }

            // Turn off LED only if no keys are pressed
            if (key_active_state == 0) {
                pico_set_led(false);
            }
        }
    }
    return 0;
}
