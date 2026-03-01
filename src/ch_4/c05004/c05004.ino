/******************************************************************
  @file       c05004.ino
  @brief      Accelerometer and Proximity Data Capture
  @author     David Such
  @copyright  Please see the accompanying LICENSE file.

  Code:        David Such
  Version:     1.0.1
  Date:        03/01/25

  1.0.0 Original Release.                         03/01/25
  1.0.1 Updated to take a sample when the space bar is pressed.

  This example captures data from the on-board BMI270 IMU and the APDS9960 proximity sensor.
  It takes a sample only when the space bar is pressed and displays it in CSV format on the Serial Monitor.

******************************************************************/

#include <Arduino_BMI270_BMM150.h> 
#include <Arduino_APDS9960.h>     

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  if (!APDS.begin()) {
    Serial.println("Failed to initialize APDS9960!");
    while (1);
  }

  // Print CSV header
  Serial.println("time,aX,aY,aZ,proximity");
}

void loop() {
  // Check if the space bar is pressed
  if (Serial.available() > 0) {
    char input = Serial.read();
    if (input == ' ') { // Space bar character
      unsigned long currentTime = millis();

      float aX, aY, aZ;
      int proximity;

      // Read accelerometer data
      if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(aX, aY, aZ);
      } else {
        aX = aY = aZ = 0; // Default to 0 if data is unavailable
      }

      // Read proximity data
      if (APDS.proximityAvailable()) {
        proximity = APDS.readProximity();
      } else {
        proximity = -1; // Default to -1 if data is unavailable
      }

      // Print data in CSV format
      Serial.print(currentTime);
      Serial.print(',');
      Serial.print(aX, 3);
      Serial.print(',');
      Serial.print(aY, 3);
      Serial.print(',');
      Serial.print(aZ, 3);
      Serial.print(',');
      Serial.println(proximity);
    }
  }
}