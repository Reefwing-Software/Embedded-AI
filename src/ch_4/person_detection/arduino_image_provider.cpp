/* Copyright 2022 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#include <algorithm>
#include <type_traits>

#include "image_provider.h"
#include "model_settings.h"
#include "tensorflow/lite/micro/micro_log.h"
#include "tensorflow/lite/micro/micro_utils.h"

#if defined(ARDUINO) && !defined(ARDUINO_NICLA_VISION)
#define ARDUINO_EXCLUDE_CODE
#endif  // defined(ARDUINO) && !defined(ARDUINO_NICLA_VISION)

#ifndef ARDUINO_EXCLUDE_CODE

#include "Arduino.h"
#include "camera.h"
#include "gc2145.h"

// Initialize the GC2145 camera
GC2145 galaxyCore;
Camera cam(galaxyCore);

namespace {

// FrameBuffer object to hold the captured frame
FrameBuffer frameBuffer;

constexpr size_t kQQVGA_width = 160;   // pixels
constexpr size_t kQQVGA_height = 120;  // pixels

constexpr size_t kImageBufferSize = kQQVGA_width * kQQVGA_height;
uint8_t image_buffer[kImageBufferSize]; // RGB565 buffer
constexpr size_t kImageBufferLength = std::extent<decltype(image_buffer)>::value;

// Initialize the camera with QQVGA resolution and RGB565 pixel format
TfLiteStatus InitCamera() {
  if (!cam.begin(CAMERA_R160x120, CAMERA_RGB565, 30)) {
    MicroPrintf("Camera initialization failed!");
    return kTfLiteError;    
  }

  cam.setVerticalFlip(true);      // Flips the image vertically
  cam.setHorizontalMirror(true);  // Mirrors the image horizontally
  
  MicroPrintf("Camera initialized successfully!");
  return kTfLiteOk;
}

// Capture a frame from the camera
TfLiteStatus CaptureFrame() {
  MicroPrintf("Capturing colour frame...");

  // Initialize the FrameBuffer object
  frameBuffer = FrameBuffer(kQQVGA_width, kQQVGA_height, 2); // 2 bytes per pixel for RGB565
  
  // Capture the frame into the FrameBuffer
  if (cam.grabFrame(frameBuffer, 5000) != 0) {
    MicroPrintf("Failed to capture frame!");
    return kTfLiteError; 
  }

  // Copy the data from the FrameBuffer into the image buffer
  memcpy(image_buffer, frameBuffer.getBuffer(), kImageBufferLength);

  MicroPrintf("Image captured");
  return kTfLiteOk;
}

// Crop and resize the image to match the model's input
TfLiteStatus CropAndResizeToGrayscale(const TfLiteTensor* tensor) {
  MicroPrintf("Cropping and resizing image to grayscale...");

  // Cropping parameters for 120x120 center square
  const size_t crop_x_start = (kQQVGA_width - kQQVGA_height) / 2;
  const size_t crop_x_end = crop_x_start + kQQVGA_height;

  // Get the input tensor buffer
  int8_t* input_buffer = tensor->data.int8;

  // Resizing and converting to grayscale
  const size_t target_width = 96;
  const size_t target_height = 96;

  for (size_t y = 0; y < target_height; y++) {
    for (size_t x = 0; x < target_width; x++) {
      // Map the target pixel to the original cropped area
      size_t src_x = crop_x_start + (x * kQQVGA_height) / target_width;
      size_t src_y = (y * kQQVGA_height) / target_height;

      // Extract RGB565 pixel from the source image
      size_t src_index = (src_y * kQQVGA_width + src_x) * 2;
      uint16_t rgb565_pixel = (image_buffer[src_index] << 8) | image_buffer[src_index + 1];

      // Convert RGB565 to grayscale
      uint8_t r = (rgb565_pixel >> 11) & 0x1F;
      uint8_t g = (rgb565_pixel >> 5) & 0x3F;
      uint8_t b = rgb565_pixel & 0x1F;
      uint8_t grayscale = (r << 3) * 0.299 + (g << 2) * 0.587 + (b << 3) * 0.114;

      // Quantize grayscale value and store it in the tensor buffer
      input_buffer[y * target_width + x] = tflite::FloatToQuantizedType<int8_t>(
          grayscale / 255.0f, tensor->params.scale, tensor->params.zero_point);
    }
  }

  MicroPrintf("Image cropped, resized, and converted to grayscale.");
  return kTfLiteOk;
}

// Get an image from the camera and process it
TfLiteStatus GetCameraImage(const TfLiteTensor* tensor) {
  static bool is_camera_initialized = false;

  if (!is_camera_initialized) {
    if (InitCamera() != kTfLiteOk) {
      MicroPrintf("InitCamera failed");
      return kTfLiteError;
    }
    is_camera_initialized = true;
  }

  if (CaptureFrame() != kTfLiteOk) {
    MicroPrintf("CaptureFrame failed");
    return kTfLiteError;
  }

  if (CropAndResizeToGrayscale(tensor) != kTfLiteOk) {
    MicroPrintf("CropAndResizeToGrayscale failed");
    return kTfLiteError;
  }

  return kTfLiteOk;
}

}  // namespace

TfLiteStatus GetImage(const TfLiteTensor* tensor) {
  return GetCameraImage(tensor);
}

#endif  // ARDUINO_EXCLUDE_CODE
