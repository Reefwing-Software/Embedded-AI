/******************************************************************
  @file       c04008.ino
  @brief      Grab sample RGB565 image from Nicla Vision camera
  @author     David Such
  @copyright  Please see the accompanying LICENSE file.

  Code:        David Such
  Version:     1.0.1

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

// Function to blink the built-in LED in case of errors
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

  // Initialize the camera with QQVGA resolution and grayscale pixel format
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
    blinkLED(5); // Blink LED 5 times to indicate error
    delay(1000);
    return;
  }

  Serial.println("Frame captured!");
  printPythonData();

  delay(2000); // Delay between frames
}

void printPythonData() {
  uint8_t* buffer = frameBuffer.getBuffer();
  if (buffer == NULL) {
    Serial.println("FrameBuffer not allocated!");
    return;
  }

  uint32_t width = 160;  // QQVGA width
  uint32_t height = 120; // QQVGA height
  uint32_t bufferSize = 0;

  Serial.println("rgb565_image = [");
  for (uint32_t y = 0; y < height; y++) {
    Serial.print("  [");
    for (uint32_t x = 0; x < width; x++) {
      // Each pixel is 2 bytes: combine the bytes to form a 16-bit RGB565 value
      uint16_t pixel = (buffer[(y * width + x) * 2] << 8) | buffer[(y * width + x) * 2 + 1];
      Serial.print(pixel);
      if (x < width - 1) Serial.print(", "); // Add comma between elements
      bufferSize += 2; // Increment the buffer size counter by 2 for each pixel
    }
    Serial.println((y < height - 1) ? "]," : "]"); // Add closing bracket and comma for all but the last row
  }
  Serial.println("]");

  // Print the calculated buffer size
  Serial.print("Calculated Frame Buffer Size: ");
  Serial.print(bufferSize);
  Serial.println(" bytes");
}
