/******************************************************************
  @file       c05009.ino
  @brief      Grab a RGB565 image from Nicla Vision camera
  @author     David Such
  @copyright  Please see the accompanying LICENSE file.

  Code:        David Such
  Version:     1.0.1
  Date:        03/01/25

  1.0.0 Original Release.                         03/01/25

  A sketch for the Arduino Nicla Vision to capture a frame at QQVGA 
  resolution in RGB565, downsample it to 96x96 grayscale, and print 
  both the original and downsampled images to the Serial Monitor.

******************************************************************/

#include "camera.h"
#include "gc2145.h"

#ifndef ARDUINO_NICLA_VISION
#error "This sketch only works on the Arduino Nicla Vision."
#endif

// Initialize the GC2145 camera
GC2145 galaxyCore;
Camera cam(galaxyCore);

// FrameBuffer object to hold the captured frame
FrameBuffer frameBuffer;

// Function to blink the built-in LED rapidly
void blinkLED(uint8_t count) {
  pinMode(LED_BUILTIN, OUTPUT);
  while (count--) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    digitalWrite(LED_BUILTIN, LOW);
    delay(100);
  }
}

void setup() {
  Serial.begin(115200);
  while (!Serial); // Wait for the Serial Monitor to open

  Serial.println("Initializing camera...");

  // Initialize the camera with QQVGA resolution and RGB565 pixel format
  if (!cam.begin(CAMERA_R160x120, CAMERA_RGB565, 30)) {
    Serial.println("Camera initialization failed!");
    blinkLED(10); // Blink LED 10 times to indicate error
    while (1);    // Halt execution
  }

  cam.setVerticalFlip(true);      // Flips the image vertically
  cam.setHorizontalMirror(true);  // Mirrors the image horizontally

  int frameSize = cam.frameSize();

  // Print the camera frame size
  Serial.print("Camera Frame Size: ");
  Serial.print(frameSize);
  Serial.println(" bytes");
  Serial.println("Camera initialized successfully!");
}

void loop() {
  Serial.println("Capturing colour frame...");

  // Capture a frame - 5000 ms is the timeout condition
  if (cam.grabFrame(frameBuffer, 5000) != 0) {
    Serial.println("Failed to capture frame!");
    blinkLED(10); // Blink LED 10 times to indicate error
    delay(3000);
    return;
  }

  // Blink LED rapidly 5 times to indicate success
  blinkLED(5);

  // Process the captured frame
  uint8_t* buffer = frameBuffer.getBuffer();
  if (buffer == NULL) {
    Serial.println("FrameBuffer not allocated!");
    return;
  }

  // Print the original QQVGA RGB565 image
  Serial.println("rgb565_image = [");
  uint32_t width = 160; // QQVGA width
  uint32_t height = 120; // QQVGA height
  for (uint32_t y = 0; y < height; y++) {
    Serial.print("  [");
    for (uint32_t x = 0; x < width; x++) {
      uint16_t pixel = (buffer[(y * width + x) * 2] << 8) | buffer[(y * width + x) * 2 + 1];
      Serial.print(pixel);
      if (x < width - 1) Serial.print(", ");
    }
    Serial.println((y < height - 1) ? "]," : "]");
  }
  Serial.println("]");

  // Crop, down-sample, and convert to grayscale
  uint32_t cropStartX = (width - height) / 2; // Center crop to square aspect ratio (120x120)
  uint32_t cropWidth = height; // Cropped width and height for square aspect ratio

  Serial.println("grayscale_image = [");
  for (uint32_t y = 0; y < 96; y++) {
    Serial.print("  [");
    for (uint32_t x = 0; x < 96; x++) {
      // Map downsampled 96x96 to cropped 120x120
      uint32_t srcX = cropStartX + x * cropWidth / 96;
      uint32_t srcY = y * cropWidth / 96;

      // Get the RGB565 pixel
      uint16_t pixel = (buffer[(srcY * width + srcX) * 2] << 8) | buffer[(srcY * width + srcX) * 2 + 1];

      // Convert to grayscale using weighted average (standard luminance calculation)
      uint8_t r = (pixel >> 11) & 0x1F;
      uint8_t g = (pixel >> 5) & 0x3F;
      uint8_t b = pixel & 0x1F;
      r = (r << 3) | (r >> 2); // Scale to 8 bits
      g = (g << 2) | (g >> 4); // Scale to 8 bits
      b = (b << 3) | (b >> 2); // Scale to 8 bits
      uint8_t gray = (0.299 * r + 0.587 * g + 0.114 * b); // Weighted grayscale conversion

      Serial.print(gray);
      if (x < 95) Serial.print(", ");
    }
    Serial.println((y < 95) ? "]," : "]");
  }
  Serial.println("]");

  delay(2000); // Wait 2 seconds before capturing the next frame
}