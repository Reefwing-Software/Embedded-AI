/******************************************************************
  @file    dc_load.ino
  @brief   Test DC Programmable Load Circuit

  Version:     1.0.0
  
  Copyright (c) 2026 David Such

  This software is released under the MIT License.
  https://opensource.org/licenses/MIT  
******************************************************************/

#include <OPAMP.h>

#define DAC_PIN     A0
#define V_PLUS      A1
#define V_MINUS     A2
#define OP_AMP_OUT  A3
#define ADC_PIN     A5

#define SENSE_RESISTOR  1.0

void setupOpAmp() {
  if (!OPAMP.begin(OPAMP_SPEED_HIGHSPEED)) {
    Serial.println("Error - Failed to start op-amp");
  }
  else {
    bool const running = OPAMP.isRunning(0);

    if (running) {
      Serial.println("Op-amp running on channel 0");
    } else {
      Serial.println("Error - Op-amp on channel 0 is not running");
    }
  }
}

void setup() {
  pinMode(ADC_PIN, INPUT);
  pinMode(DAC_PIN, OUTPUT);

  Serial.begin(115200);
  while (!Serial);

  setupOpAmp();
  analogReadResolution(10);   // ADC 10-bit resolution (0-1023)
  analogWriteResolution(8);   // DAC 8-bit resolution (0-255)
  analogWrite(DAC_PIN, 0);    // Turn DAC output off
}

int readADC(int pin) {
    analogRead(pin);        // First "dummy" read to allow stabilization
    delayMicroseconds(10);  
    return analogRead(pin); // Second read for more accurate value
}

void loop() {
  // Sweep DAC voltage from 0V to 5V in 0.1V increments
  for (float dacVoltage = 0; dacVoltage <= 5.0; dacVoltage += 0.1) {
    // Set DAC output based on desired voltage
    int dacValue = (int)(dacVoltage * 255.0 / 5.0);

    analogWrite(DAC_PIN, dacValue);

    // Read voltage across the sense resistor using the ADC
    int adcValue = readADC(ADC_PIN);
    float senseVoltage = adcValue * (5.0 / 1023.0);  // Convert ADC reading to voltage

    // Calculate the current through the sense resistor
    float current = senseVoltage / SENSE_RESISTOR;

    // Output DAC voltage, sense resistor voltage, and calculated current to serial monitor
    Serial.print("DAC Voltage: ");
    Serial.print(dacVoltage, 2);
    Serial.print(" V, Sense Voltage: ");
    Serial.print(senseVoltage, 2);
    Serial.print(" V, Sense Current: ");
    Serial.print(current * 1000, 2);  // Convert to mA for readability
    Serial.println(" mA");

    delay(500);  // Wait half a second before the next step
  }

  analogWrite(DAC_PIN, 0);    // Turn DAC output off
  Serial.println("\nSweep Completed");
  while(1);  // Loop forever
}
