/******************************************************************
  @file       c05005.ino
  @brief      Near Ear Neural Network Prediction
  @author     David Such
  @copyright  Please see the accompanying LICENSE file.

  Code:        David Such
  Version:     1.0.1
  Date:        03/01/25

  1.0.0 Original Release.                         03/01/25

******************************************************************/

#include <Arduino_BMI270_BMM150.h> 
#include <Arduino_APDS9960.h>   
#include <TensorFlowLite.h>

// TensorFlow Lite Micro library requirements
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_log.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"

#include "near_ear_model.h"

// TensorFlow Lite Model and Interpreter
namespace {
const tflite::Model* model;
tflite::MicroInterpreter *interpreter;
TfLiteTensor *input_tensor;
TfLiteTensor *output_tensor;

constexpr int kTensorArenaSize = 2048;     // Memory size for the model's tensors
alignas(16) uint8_t tensor_arena[kTensorArenaSize];  // Keep aligned to 16 bytes for CMSIS
}  // namespace

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  if (!APDS.begin()) {
    Serial.println("Failed to initialize APDS9960!");
    while (1);
  }

  // Initialize the error reporter
  Serial.println("Initializing TensorFlow Lite Micro interpreter...");

  tflite::InitializeTarget();

  // Load the TensorFlow Lite model from the header file
  model = tflite::GetModel(ne_model);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    Serial.print("Model schema version mismatch! Expected ");
    Serial.print(TFLITE_SCHEMA_VERSION);
    Serial.print(", but got ");
    Serial.println(model->version());
    while (1); // Halt execution
  }

  static tflite::AllOpsResolver resolver;

  // Create the interpreter
  static tflite::MicroInterpreter static_interpreter(
      model, resolver, tensor_arena, kTensorArenaSize);
  interpreter = &static_interpreter;

  // Allocate memory for the model's input and output tensors
  TfLiteStatus allocate_status = interpreter->AllocateTensors();
  if (allocate_status != kTfLiteOk) {
    Serial.println("Failed to allocate tensors!");
    while (1); // Halt execution
  }

  // Get pointers to the model's input and output tensors
  input_tensor = interpreter->input(0);
  output_tensor = interpreter->output(0);

  Serial.println("Model is ready for inference.");
}

void loop() {

  float aX, aY, aZ;
  int proximity;

  // Read accelerometer data
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(aX, aY, aZ);
  } 
  else {
    aX = aY = aZ = 0; 
  }

  // Read proximity data
  if (APDS.proximityAvailable()) {
    proximity = APDS.readProximity();
  } 
  else {
    proximity = -1; // Default to -1 if data is unavailable
  }

  // Normalize inputs to match training preprocessing
  input_tensor->data.f[0] = (aX + 1.0) / 2.0; // Normalize to [0, 1]
  input_tensor->data.f[1] = (aY + 1.0) / 2.0; // Normalize to [0, 1]
  input_tensor->data.f[2] = (aZ + 1.0) / 2.0; // Normalize to [0, 1]
  input_tensor->data.f[3] = proximity / 255.0; // Normalize to [0, 1]

  // Run inference
  TfLiteStatus invoke_status = interpreter->Invoke();
  if (invoke_status != kTfLiteOk) {
    Serial.println("Failed to invoke the model!");
    return;
  }

  // Get the output prediction
  float prediction = output_tensor->data.f[0];

  // Print the result
  Serial.print("Prediction: ");
  Serial.println(prediction);

  // Delay for readability
  delay(1000);
}
