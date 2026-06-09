/******************************************************************
  @file    transfer_characteristics.ino
  @brief   Plot the MOSFET Vgs vs Ids

  Version:     1.0.0

  Copyright (c) 2026 David Such

  This software is released under the MIT License.
  https://opensource.org/licenses/MIT  
******************************************************************/

#define DAC_PIN A0          // DAC output pin
#define ADC_PIN A5          // ADC input pin to read the sense resistor voltage
#define SENSE_RESISTOR 4.7  // Sense resistor value in ohms
#define VBAT 4.2            // Battery Supply voltage


void setup() {
  pinMode(ADC_PIN, INPUT);
  pinMode(DAC_PIN, OUTPUT);

  Serial.begin(115200);
  while (!Serial);  // Wait for serial connection

  analogReadResolution(10);  // Set ADC to 10-bit resolution (0-1023)
  analogWriteResolution(8);  // Set DAC to 8-bit resolution (0-255)
  analogWrite(DAC_PIN, 0);    // Turn DAC output off
}

int readADC(int pin) {
    analogRead(pin);        // First "dummy" read to allow stabilization
    delayMicroseconds(10);  
    return analogRead(pin); // Second read for more accurate value
}

void loop() {
  // Sweep DAC voltage from 0V to 5V in 0.1V increments
  for (float vgs = 0; vgs <= 5.0; vgs += 0.1) {
    // Calculate the DAC value to output the desired Vgs
    int dacValue = (int)(vgs * 255.0 / 5.0);
    analogWrite(DAC_PIN, dacValue);

    // Read the voltage across the sense resistor
    int adcValue = readADC(ADC_PIN);
    float voltageAtDrain = adcValue * (5.0 / 1023.0);

    // Calculate the voltage across the sense resistor
    float senseVoltage = VBAT - voltageAtDrain;

    // Calculate the drain-source current Ids
    float ids = senseVoltage / SENSE_RESISTOR;

    // Output Vgs and Ids to the serial monitor
    Serial.print("Vgs: ");
    Serial.print(vgs, 2);  // Print Vgs in volts with 2 decimal places
    Serial.print(" V, Ids: ");
    Serial.print(ids * 1000, 2);  // Print Ids in mA with 2 decimal places
    Serial.println(" mA");

    delay(500);  // Wait half a second before the next step
  }

  analogWrite(DAC_PIN, 0);    // Turn DAC output off
  Serial.println("\nSweep Completed");
  while(1);  // Loop forever
}