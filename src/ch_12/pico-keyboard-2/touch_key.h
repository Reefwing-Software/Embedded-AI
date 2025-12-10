// Copyright (c) 2025 David Such
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT
//
// A capacitive touch class derived from CircuitPython's touchio
// ref: https://github.com/adafruit/circuitpython/blob/main/shared-module/touchio/TouchIn.c

#include "pico/stdlib.h"
#include "hardware/gpio.h"

#define N_SAMPLES 10        // Number of samples to average
#define CHARGE_MICROS 10    // Time to charge the pad
#define TIMEOUT_TICKS 10000 // Max wait time for discharge

class TouchKey
{
public:
    TouchKey() {}

    // Initialize a pin for touch sensing
    void begin(int pin, uint16_t debounce_millis = 10) {
        pin = pin;
        debounce_interval = debounce_millis;
        last_state = false;
        changed = false;
        last_debounce_micros = time_us_32();

        gpio_init(pin);
        gpio_set_dir(pin, GPIO_IN); // Initially set as input
        recalibrate();
    }

    // Recalibrate the baseline threshold for touch detection
    void recalibrate() {
        const int num_reads = 5;
        raw_value = 0;
        for (int i = 0; i < num_reads; i++)
        {
            raw_value += rawRead();
        }
        raw_value /= num_reads;
        threshold = raw_value * 1.05; // Increase threshold slightly
    }

    // Call update frequently to debounce the touch state
    void update() {
        changed = false;
        uint32_t now = time_us_32();
        if ((now - last_debounce_micros) / 1000 > debounce_interval)
        {
            last_debounce_micros = now;
            bool touch_state = isTouched();
            changed = touch_state != last_state;
            last_state = touch_state;
        }
    }

    // Returns true if touch event just started
    bool rose() {
        return changed && last_state == true;
    }

    // Returns true if touch event just ended
    bool fell() {
        return changed && last_state == false;
    }

    // Check if the pad is currently touched
    bool isTouched() {
        raw_value = rawRead();
        return (raw_value > threshold);
    }

    // Perform the actual capacitive sensing
    int16_t rawRead() {
        uint16_t ticks = 0;
        for (uint16_t i = 0; i < N_SAMPLES; i++)
        {
            // Charge the pad
            gpio_set_dir(pin, GPIO_OUT);
            gpio_put(pin, 1);
            sleep_us(CHARGE_MICROS);

            // Set back to input and count discharge time
            gpio_set_dir(pin, GPIO_IN);
            while (gpio_get(pin)) {
                if (ticks >= TIMEOUT_TICKS) {
                    return TIMEOUT_TICKS;
                }
                ticks++;
            }
        }
        return ticks;
    }

    uint16_t getThreshold() const {
        return threshold;
    }

    void setThreshold(uint16_t value) {
        threshold = value;
    }


private:
    uint32_t last_debounce_micros;
    uint16_t debounce_interval;
    bool last_state;
    bool changed;
    uint16_t threshold;
    int pin;
    uint16_t raw_value;
};