// Copyright (c) 2026 David Such
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

#include <stdio.h>

#include "pico/stdlib.h"
#include "touch.pio.h"
#include "bsp/board_api.h"
#include "tusb.h"

//--------------------------------------------------------------------+
// DEFINITIONS
//--------------------------------------------------------------------+

#define TOUCH_PIO pio0         // PIO instance for touch sensing
#define TOUCH_PIN 2            // GPIO number for the first touch button
#define TOUCH_NUMBER 14        // Number of sequential touch buttons
#define TOUCH_SM_COUNT ((TOUCH_NUMBER + 4) / 5)  // State machines required
#define CLOCK_DIV 40           // Clock divider for PIO - tune for sensitivity
#define DRIVE_STRENGTH 4       // Drive strength: 2mA, 4mA, 8mA, or 12mA
#define FAST_SLEW false        // Slew rate: true (fast), false (slow)

#ifdef CYW43_WL_GPIO_LED_PIN
// Pico W devices use a GPIO on the WIFI chip for the LED.
#include "pico/cyw43_arch.h"
#endif

#define MAX_ARP_NOTES 32       // Maximum notes in an arpeggio sequence

typedef enum {
    CHORD_MAJOR,
    CHORD_MINOR,
    CHORD_DIMINISHED,
    CHORD_AUGMENTED,
    CHORD_SEVENTH
} ChordType;

enum  {
  BLINK_NOT_MOUNTED = 250,
  BLINK_MOUNTED = 1000,
  BLINK_SUSPENDED = 2500,
};

int octave_offset = 0;      // Default octave shift, 0 means middle C (C3)
uint key_active_state = 0;  // Track which keys are currently pressed
static uint32_t blink_interval_ms = BLINK_NOT_MOUNTED;
static bool led_on_due_to_touch = false; 
volatile uint touch_state = 0;
volatile uint touch_state_last = 0;
volatile bool touch_change_flg = false;
volatile bool arpeggio_active = false;  // Flag for arpeggio sequence
size_t arpeggio_size = 0;               // Stores size of generated sequence
uint8_t arpeggio_sequence[MAX_ARP_NOTES];

//--------------------------------------------------------------------+
// FUNCTION PROTOTYPES
//--------------------------------------------------------------------+

int pico_led_init(void);
void pico_set_led(bool led_on);
int touch_setup(PIO pio_touch, int num_buttons, int start_pin, float clk_div, uint drive_strength, bool fast_slew);
void touch_isr_handler(void);
void touch_handler(void);
void led_blinking_task(void);
void midi_send(uint8_t note, uint8_t velocity, bool note_on);
void midi_sequence(const uint8_t* note_sequence, size_t sequence_size);
int generate_arpeggio(uint8_t root_note, ChordType chord_type, uint8_t num_cycles, uint8_t* note_sequence, size_t max_size);

//--------------------------------------------------------------------+
// MAIN
//--------------------------------------------------------------------+

int main() {
  board_init();
  tusb_init();
  pico_led_init();
  touch_setup(TOUCH_PIO, TOUCH_NUMBER, TOUCH_PIN, CLOCK_DIV, DRIVE_STRENGTH, FAST_SLEW);

  while (true) {
    tud_task();
    led_blinking_task();
    touch_handler();

    if (arpeggio_active) {
        midi_sequence(arpeggio_sequence, arpeggio_size);
    }
  }
}

//--------------------------------------------------------------------+
// USB Device callbacks
//--------------------------------------------------------------------+

// Invoked when device is mounted
void tud_mount_cb(void) {
  blink_interval_ms = BLINK_MOUNTED;
}

// Invoked when device is unmounted
void tud_umount_cb(void) {
  blink_interval_ms = BLINK_NOT_MOUNTED;
}

// Invoked when usb bus is suspended
// remote_wakeup_en : if host allow us to perform remote wakeup
// Within 7ms, device must draw an average of current less than 2.5 mA from bus
void tud_suspend_cb(bool remote_wakeup_en) {
  (void) remote_wakeup_en;
  blink_interval_ms = BLINK_SUSPENDED;
}

// Invoked when usb bus is resumed
void tud_resume_cb(void) {
    blink_interval_ms = tud_mounted() ? BLINK_MOUNTED : BLINK_NOT_MOUNTED;
}

//--------------------------------------------------------------------+
// MIDI Message Handler
//--------------------------------------------------------------------+

void midi_send(uint8_t note, uint8_t velocity, bool note_on) {
    uint8_t msg[3];

    // Determine MIDI command: Note On or Note Off
    msg[0] = note_on ? 0x90 : 0x80;  // 0x90 = Note On, 0x80 = Note Off
    msg[1] = note;                   // MIDI Note Number
    msg[2] = velocity;               // Velocity (0 if Note Off)

    // Send MIDI message
    tud_midi_n_stream_write(0, 0, msg, 3);
}

// Variable that holds the current position in the sequence.
uint32_t note_pos = 0;

// Store example melody as an array of note values
uint8_t test_note_sequence[] = {
  74,78,81,86,90,93,98,102,57,61,66,69,73,78,81,85,88,92,97,100,97,92,88,85,81,78,
  74,69,66,62,57,62,66,69,74,78,81,86,90,93,97,102,97,93,90,85,81,78,73,68,64,61,
  56,61,64,68,74,78,81,86,90,93,98,102
};

void midi_sequence(const uint8_t* note_sequence, size_t sequence_size) {
  static uint32_t start_ms = 0;
  static uint32_t note_pos = 0;

  // Send note every 286 ms
  if (board_millis() - start_ms < 286) return; // Not enough time
  start_ms += 286;

  // Previous position in the note sequence
  int previous = note_pos - 1;

  // If we currently are at position 0, set the previous position to the last note in the sequence
  if (previous < 0) previous = sequence_size - 1;

  // Send Note On for current position at full velocity (127) on channel 1.
  midi_send(note_sequence[note_pos], 127, true);
  midi_send(note_sequence[previous], 0, false); // Send Note Off for previous note

  // Increment position
  note_pos++;

  // If we are at the end of the sequence, reset
  if (note_pos >= sequence_size) {
    arpeggio_active = false;  // Disable arpeggio mode
    note_pos = 0;
  }
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

bool pico_led_state() {
  return led_on_due_to_touch;
}

void led_blinking_task(void) {
  static uint32_t start_ms = 0;
  static bool led_state = false;

  // If a key is pressed, keep the LED solid and skip blinking
  if (pico_led_state()) { 
    return; 
  }

  // Blink every interval ms
  if (board_millis() - start_ms < blink_interval_ms) return; // Not enough time
  start_ms += blink_interval_ms;

  board_led_write(led_state);
  led_state = !led_state; // Toggle LED state
}

//--------------------------------------------------------------------+
// TOUCH SENSING
//--------------------------------------------------------------------+
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

void touch_handler(void) {
    if (touch_change_flg) {
      touch_change_flg = false;
  
      uint new_keys_pressed = touch_state & ~key_active_state;  // Newly pressed keys
      uint keys_released = key_active_state & ~touch_state;     // Keys that were released
  
      // Update the active key state
      key_active_state = touch_state;
  
      // Iterate over all keys
      for (int i = 0; i < TOUCH_NUMBER; i++) {
          if (new_keys_pressed & (1 << i)) {
              if (i == 11) {          // GP13: "Arpeggio" button
                arpeggio_size = generate_arpeggio(48, CHORD_SEVENTH, 10, arpeggio_sequence, MAX_ARP_NOTES);
                if (arpeggio_size > 0) {
                    arpeggio_active = true; // Start playing in main loop
                }
              } else if (i == 12) {   // GP14: "Octave -" Lower limit at MIDI 0
                  octave_offset = (octave_offset - 12 < -48) ? -48 : (octave_offset - 12);
              } else if (i == 13) {   // GP15: "Octave +" Upper limit at MIDI 127
                  octave_offset = (octave_offset + 12 > 48) ? 48 : (octave_offset + 12);
              } else {
                  // Send MIDI Note On for note keys only (GP2-GP13)
                  uint8_t note = 48 + octave_offset + i;  // MIDI Note C3 (48) + offset
                  midi_send(note, 127, true);
              }
          }
  
          if (keys_released & (1 << i)) {
              if (i < 12) {  // Only release note keys (GP2-GP13)
                  uint8_t note = 48 + octave_offset + i;
                  midi_send(note, 0, false);
              }
          }
      }
  
      // Turn LED on while any key (note or octave) is pressed
      if (key_active_state != 0) {
          pico_set_led(true);
      } else {
          pico_set_led(false);
      }
    }
  }

//--------------------------------------------------------------------+
// ARPEGGIATOR
//--------------------------------------------------------------------+
int generate_arpeggio(uint8_t root_note, ChordType chord_type, uint8_t num_cycles, uint8_t* note_sequence, size_t max_size) {
    int chord_intervals[4] = {0, 0, 0, 0};  // Holds up to 4 intervals
    uint8_t num_notes = 0;

    // Define chord intervals based on type
    switch (chord_type) {
        case CHORD_MAJOR:
            chord_intervals[0] = 0;  // Root
            chord_intervals[1] = 4;  // Major Third
            chord_intervals[2] = 7;  // Perfect Fifth
            num_notes = 3;
            break;
        case CHORD_MINOR:
            chord_intervals[0] = 0;
            chord_intervals[1] = 3;  // Minor Third
            chord_intervals[2] = 7;
            num_notes = 3;
            break;
        case CHORD_DIMINISHED:
            chord_intervals[0] = 0;
            chord_intervals[1] = 3;
            chord_intervals[2] = 6;  // Diminished Fifth
            num_notes = 3;
            break;
        case CHORD_AUGMENTED:
            chord_intervals[0] = 0;
            chord_intervals[1] = 4;
            chord_intervals[2] = 8;  // Augmented Fifth
            num_notes = 3;
            break;
        case CHORD_SEVENTH:
            chord_intervals[0] = 0;
            chord_intervals[1] = 4;
            chord_intervals[2] = 7;
            chord_intervals[3] = 10;  // Minor Seventh
            num_notes = 4;
            break;
        default:
            return -1; // Invalid chord type
    }

    // Generate the arpeggio sequence
    size_t index = 0;
    for (int cycle = 0; cycle < num_cycles; cycle++) {
        for (int i = 0; i < num_notes; i++) {
            if (index < max_size) {
                note_sequence[index++] = root_note + chord_intervals[i];
            }
        }
    }

    return index; // Return the number of notes in the sequence
}
