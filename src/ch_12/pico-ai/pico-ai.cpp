#include "pico/stdlib.h"
#include "touch.pio.h"

#include "tflite_model.h"
#include "tensorflow/lite/core/c/common.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_log.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/micro_profiler.h"
#include "tensorflow/lite/micro/recording_micro_interpreter.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"

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

// Note the Pico W uses GPIO on the WIFI chip for the LED.
#ifdef CYW43_WL_GPIO_LED_PIN
#include "pico/cyw43_arch.h"
#endif

//--------------------------------------------------------------------+
// GLOBAL DECLARATIONS
//--------------------------------------------------------------------+

// Key labels corresponding to the 14 touch buttons
const char *key_labels[TOUCH_NUMBER] = {
    "C", "C#", "D", "D#", "E", "F", 
    "F#", "G", "G#", "A", "A#", "B", 
    "AI", "Octave +"
};

volatile uint touch_state = 0;
volatile uint touch_state_last = 0;
volatile bool touch_change_flg = false;

// Capacitive touch key states
bool gan_inference_flg = false;
int8_t octave_offset = 0;   // Tracks octave shifts, default = 0 (Middle C)
uint key_active_state = 0;

// Tensorflow Lite Micro variables
namespace {
    const tflite::Model* model = nullptr;
    tflite::MicroInterpreter* interpreter = nullptr;
    TfLiteTensor* input = nullptr;
    TfLiteTensor* output = nullptr;
    int inference_count = 0;

    constexpr int kTensorArenaSize = 4096; // 4 KB
    uint8_t tensor_arena[kTensorArenaSize];

    int8_t seed_notes[1000] = {0}; 
    int8_t zero_point = 1;
    float scale = 1.0f;
}  // namespace

//--------------------------------------------------------------------+
// LED CONTROL
//--------------------------------------------------------------------+
int pico_led_init(void) {
#if defined(PICO_DEFAULT_LED_PIN)
    // The Pico uses a GPIO for the LED and defines PICO_DEFAULT_LED_PIN
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
    return PICO_OK;
#elif defined(CYW43_WL_GPIO_LED_PIN)
    // For Pico W devices we need to initialise the driver etc
    return cyw43_arch_init();
#else
    // No default LED pin for this device.
    return PICO_ERROR_IO;
#endif
}

void pico_set_led(bool led_on) {
#if defined(PICO_DEFAULT_LED_PIN)
    gpio_put(PICO_DEFAULT_LED_PIN, led_on);
#elif defined(CYW43_WL_GPIO_LED_PIN)
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, led_on);
#endif
}

//--------------------------------------------------------------------+
// USB SERIAL
//--------------------------------------------------------------------+

void wait_for_usb_serial() {
    while (!stdio_usb_connected()) {
        sleep_ms(10);  // Wait for USB serial connection
    }
}

//--------------------------------------------------------------------+
// GAN GENERATOR SETUP AND INFERENCE FUNCTIONS
//--------------------------------------------------------------------+
void gan_setup() {
    tflite::InitializeTarget();

    MicroPrintf("Loading MIDI Generator Model...\n");

    // Map the model into a usable data structure.
    model = tflite::GetModel(tflite_model);
    if (model->version() != TFLITE_SCHEMA_VERSION) {
        MicroPrintf(
            "Model provided is schema version %d not equal "
            "to supported version %d.",
            model->version(), TFLITE_SCHEMA_VERSION);
        return;
    }

    MicroPrintf("Model loaded successfully");

    // This pulls in all the operation implementations we need.
    static tflite::MicroMutableOpResolver<4> resolver;

    resolver.AddFullyConnected();   // Registers Dense layers
    resolver.AddLeakyRelu();        // Registers Leaky ReLU activation
    resolver.AddReshape();          // Registers Reshape operation
    resolver.AddTanh();             // Registers Tanh activation

    MicroPrintf("Operations registered successfully");

    // Build an interpreter to run the model with.
    static tflite::MicroInterpreter static_interpreter(
        model, resolver, tensor_arena, kTensorArenaSize);
    interpreter = &static_interpreter;

    // Allocate memory from the tensor_arena for the model's tensors.
    TfLiteStatus allocate_status = interpreter->AllocateTensors();

    MicroPrintf("Estimated Memory Needed: %d bytes", interpreter->arena_used_bytes());

    if (allocate_status != kTfLiteOk) {
        MicroPrintf("AllocateTensors() failed");
        return;
    }

    // Obtain pointers to the model's input and output tensors.
    input = interpreter->input(0);
    output = interpreter->output(0);

    // Print input tensor dimensions
    MicroPrintf("Input tensor dimensions: %d", input->dims->size);
    for (int i = 0; i < input->dims->size; i++) {
        MicroPrintf("Dim %d: %d", i, input->dims->data[i]);
    }

    zero_point = input->params.zero_point;
    scale = input->params.scale;

    MicroPrintf("Input zero point: %d, scale: %f", zero_point, scale);

    // Generate default random seed notes [-128, 127]
    for (int i = 0; i < 1000; i++) {
        seed_notes[i] = static_cast<int8_t>((rand() % 256) - 128 + zero_point);
    }

    // Keep track of how many inferences we have performed.
    inference_count = 0;

    MicroPrintf("Inference model complete\n");
}

void run_gan_inference(int8_t* seed_notes, size_t seed_size) {
    MicroPrintf("Starting inference: %d\n", inference_count);
    pico_set_led(true);

    // Ensure input tensor size matches seed size
    if (seed_size > input->bytes) {
        MicroPrintf("Seed size exceeds input tensor capacity!\n");
        return;
    }

    // Copy seed notes into model input tensor
    memcpy(input->data.int8, seed_notes, seed_size);

    // Run inference
    TfLiteStatus invoke_status = interpreter->Invoke();
    if (invoke_status != kTfLiteOk) {
        MicroPrintf("Invoke() failed");
        return;
    }

    // Display the output array
    int8_t* output_data = output->data.int8;
    MicroPrintf("Generated Output Notes:\n");

    for (int i = 0; i < 100; i++) {
        MicroPrintf("Output[%d]: %d ", i, output_data[i]);
    }

    MicroPrintf("\n");
    pico_set_led(false);
    inference_count++;
}

//--------------------------------------------------------------------+
// TOUCH SENSING
//--------------------------------------------------------------------+
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

int touch_setup(PIO pio_touch, int num_buttons, int start_pin, float clk_div, uint drive_strength, bool fast_slew) {
    
    int sm;
    uint offset_touch = pio_add_program(TOUCH_PIO, &touch_program);
    
    MicroPrintf("Initializing touch keys...\n");
    for (int i = 0; i < TOUCH_SM_COUNT; i++) {
        sm = pio_claim_unused_sm(pio_touch, true);
  
        if (sm < 0) {  
            MicroPrintf("Error: No available state machines\n");
            return 1;  
        }
        
        pio_set_irq0_source_enabled(pio_touch, (pio_interrupt_source_t)sm, true);
        touch_init(pio_touch, sm, offset_touch, start_pin + (i * 5), 5, clk_div, drive_strength, fast_slew);
        pio_sm_set_enabled(pio_touch, sm, true);
    }
  
    irq_set_exclusive_handler(PIO0_IRQ_0, touch_isr_handler);
    irq_set_enabled(PIO0_IRQ_0, true);
    
    return 0;
}

void add_note_to_seed(uint8_t note_index, int octave_offset) {
    static int seed_index = 0; // Tracks current position in seed_notes array

    // Define MIDI base note for C3 (48) and adjust based on key pressed
    uint8_t midi_note = 48 + note_index + (octave_offset * 12);

    // Quantize the note using the GAN model’s expected input range
    int8_t quantized_note = static_cast<int8_t>((midi_note - 48) / 2) + zero_point; 

    seed_notes[seed_index] = quantized_note;
    seed_index = (seed_index + 1) % 1000; 
}

void touch_handler(void) {
    if (touch_change_flg) {
        touch_change_flg = false;

        // If new keys are pressed, assume all other keys were released
        uint new_keys_pressed = touch_state & ~key_active_state;  // Newly pressed keys
        uint keys_released = key_active_state & ~touch_state;     // Keys that were released

        // If any new key is pressed, all other keys are considered released
        if (new_keys_pressed) {
            keys_released = key_active_state & ~new_keys_pressed;
        }

        // Update the active key state
        key_active_state = touch_state;

        // Print newly pressed keys
        if (new_keys_pressed) {
            for (int i = 0; i < TOUCH_NUMBER; i++) {
                if (new_keys_pressed & (1 << i)) {
                    if (i < 12) { 
                        // Process note keys (C-B)
                        add_note_to_seed(i, octave_offset);
                    } else if (i == 12) { 
                        // "AI" key pressed – trigger AI-based composition
                        gan_inference_flg = true;  // Enable the AI inference function in the main loop
                    } else if (i == 13) { 
                        // "Octave +" key pressed – shift octave up
                        octave_offset = (octave_offset + 1 > 4) ? 4 : (octave_offset + 1); // Limit to 4 octaves up
                    }
                }
            }
        }

        // Turn off LED only if no keys are pressed
        pico_set_led(key_active_state != 0);
    }
}

//--------------------------------------------------------------------+
// MAIN
//--------------------------------------------------------------------+

int main()
{
    pico_led_init();
    tflite::InitializeTarget();

    wait_for_usb_serial();
    touch_setup(TOUCH_PIO, TOUCH_NUMBER, TOUCH_PIN, CLOCK_DIV, DRIVE_STRENGTH, FAST_SLEW);
    gan_setup();

    while (true) {
        touch_handler();

        // Run inference if the AI key is pressed
        if (gan_inference_flg) {
            run_gan_inference(seed_notes, sizeof(seed_notes));
            gan_inference_flg = false;
            sleep_ms(500);
        }
    }
    
    return 0;
}