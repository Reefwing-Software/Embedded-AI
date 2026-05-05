#include "pico/stdlib.h"

#include "tflite_model.h"
#include "tensorflow/lite/core/c/common.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_log.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/micro_profiler.h"
#include "tensorflow/lite/micro/recording_micro_interpreter.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"

namespace {
    const tflite::Model* model = nullptr;
    tflite::MicroInterpreter* interpreter = nullptr;
    TfLiteTensor* input = nullptr;
    TfLiteTensor* output = nullptr;
    int inference_count = 0;

    constexpr int kTensorArenaSize = 4096; // 4 KB
    uint8_t tensor_arena[kTensorArenaSize];
}  // namespace

// Note the Pico W uses GPIO on the WIFI chip for the LED.
#ifdef CYW43_WL_GPIO_LED_PIN
#include "pico/cyw43_arch.h"
#endif

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

void wait_for_usb_serial() {
    while (!stdio_usb_connected()) {
        sleep_ms(10);  // Wait for USB serial connection
    }
}

int main()
{
    int rc = pico_led_init();
    hard_assert(rc == PICO_OK);
    tflite::InitializeTarget();
    wait_for_usb_serial();
    MicroPrintf("Loading MIDI Generator Model...\n");

    // Map the model into a usable data structure.
    model = tflite::GetModel(tflite_model);
    if (model->version() != TFLITE_SCHEMA_VERSION) {
        MicroPrintf(
            "Model provided is schema version %d not equal "
            "to supported version %d.",
            model->version(), TFLITE_SCHEMA_VERSION);
        return kTfLiteError;
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
        return kTfLiteError;
    }

    // Obtain pointers to the model's input and output tensors.
    input = interpreter->input(0);
    output = interpreter->output(0);

    // Keep track of how many inferences we have performed.
    inference_count = 0;

    MicroPrintf("Inference model complete\n");

    while (true) {
        MicroPrintf("Starting inference: %d\n", inference_count);
        pico_set_led(true);

        // Generate input noise directly in int8 range [-128, 127]
        // If the model’s zero_point is not 0, we need to center the noise.
        int8_t input_data[1000];
        int8_t zero_point = input->params.zero_point;

        for (int i = 0; i < 1000; i++) {
            input_data[i] = static_cast<int8_t>((rand() % 256) - 128 + zero_point);
        }

        // Copy input data to model and run inference
        memcpy(input->data.int8, input_data, sizeof(input_data));
        TfLiteStatus invoke_status = interpreter->Invoke();

        if (invoke_status != kTfLiteOk) {
            MicroPrintf("Invoke() failed");
            return kTfLiteError;
        }
        
        // Display the output array
        int8_t* output_data = output->data.int8; // Points to output array

        for (int i = 0; i < 100; i++) {
            MicroPrintf("Output[%d]: %d, ", i, output_data[i]);
        }
        MicroPrintf("\n");
        pico_set_led(false);
        sleep_ms(500);
        inference_count++;
    }
    
    return 0;
}
