// Copyright (c) 2026 David Such
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

const int dacPin = A0;  // DAC output pin (A0)
const int testDelay = 500;  // Delay time between tests (in milliseconds)

void setup() {
  pinMode(dacPin, OUTPUT);   // Set the DAC pin as an output
}

void loop() {
  // Output minimum value in 8-bit mode (0)
  analogWrite(dacPin, 0);
  delay(testDelay);

  // Output maximum value in 8-bit mode (255)
  analogWrite(dacPin, 255);
  delay(testDelay);
  
  // Output minimum value in 12-bit mode (0)
  analogWriteResolution(12);  
  analogWrite(dacPin, 0);
  delay(testDelay);

  // Output maximum value in 12-bit mode (4095)
  analogWrite(dacPin, 4095);
  delay(testDelay);

  // Reset back to 8-bit mode for next cycle
  analogWriteResolution(8);   
}
