// Copyright (c) 2026 David Such
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

// Sketch c09006.ino
// Test it Out: Anomaly Detection and Handling
// An Arduino sketch to read the ISM330BX MLC output register 

#include <Wire.h>

// I2C address of ISM330BX (0x6A if SA0 is low, 0x6B if high)
#define ISM330BX_ADDR 0x6A

// Register address for Decision Tree 1 output
#define MLC1_SRC 0x70

uint8_t readRegister(uint8_t reg) {
  Wire.beginTransmission(ISM330BX_ADDR);
  Wire.write(reg);
  Wire.endTransmission(false);  // Restart condition
  Wire.requestFrom(ISM330BX_ADDR, (uint8_t)1);

  if (Wire.available()) {
    return Wire.read();
  } else {
    Serial.println("Error: No data received");
    return 0xFF;  // Indicate error
  }
}

void setup() {
  Serial.begin(115200);
  Wire.begin();

  delay(100);  // Allow sensor to settle
  Serial.println("Reading ISM330BX MLC1 output...");
}

void loop() {
  uint8_t classID = readRegister(MLC1_SRC);

  Serial.print("Decision Tree 1 Output: ");
  Serial.println(classID);

  delay(1000);  // Check every second
}
