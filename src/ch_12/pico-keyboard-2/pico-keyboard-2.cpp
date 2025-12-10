#include <stdio.h>
#include <algorithm> // For std::min and std::max

#include "pico/stdlib.h"
#include "touch_key.h"

constexpr int touch_threshold_offset = 300;  // Compile-time constant
const int key_pins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
constexpr size_t key_count = sizeof(key_pins) / sizeof(key_pins[0]);

// Key labels corresponding to the 14 touch buttons
const char *key_labels[key_count] = {
    "C", "C#", "D", "D#", "E", "F", 
    "F#", "G", "G#", "A", "A#", "B", 
    "Octave -", "Octave +"
};

// Declare an array of TouchKey objects
TouchKey key_array[key_count];

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

void touch_init(void) {
    // Delay to let power stabilize before touch calibration
    sleep_ms(1000);
  
    // Initialize touch buttons
    for (size_t i = 0; i < key_count; i++) {
        key_array[i].begin(key_pins[i]);
        key_array[i].setThreshold(key_array[i].getThreshold() + touch_threshold_offset);  
    }
  }

int main()
{
    stdio_init_all();
    pico_led_init();
    touch_init();

    wait_for_usb_serial();
    printf("Initializing touch keys...\n");

    int midi_base_note = 48;  // Default to C3
    const int midi_velocity = 127; 
    const int octave_step = 12;
    const int min_midi_note = 0;
    const int max_midi_note = 108;

    while (true) {
        bool any_key_pressed = false;

        for (size_t i = 0; i < key_count; i++) {
            key_array[i].update(); // Update touch state

            if (key_array[i].rose()) {  // Key pressed
                printf("Press: %s\n", key_labels[i]);
                any_key_pressed = true;

                if (i == 12) { // "Octave -" button
                    midi_base_note = std::max(midi_base_note - octave_step, min_midi_note);
                    printf("Octave Down: New base note = %d\n", midi_base_note);
                } 
                else if (i == 13) { // "Octave +" button
                    midi_base_note = std::min(midi_base_note + octave_step, max_midi_note);
                    printf("Octave Up: New base note = %d\n", midi_base_note);
                } 
                else { // Regular note press
                    //midi_send(midi_base_note + i, midi_velocity, true);
                }
            }

            if (key_array[i].fell()) {  // Key released
                printf("Release: %s\n", key_labels[i]);

                if (i < 12) { // Regular note release
                    //midi_send(midi_base_note + i, midi_velocity, false);
                }
            }
        }

        // Update LED state
        pico_set_led(any_key_pressed);

        sleep_ms(10); // Small delay to prevent excessive CPU load
    }

    return 0;
}
