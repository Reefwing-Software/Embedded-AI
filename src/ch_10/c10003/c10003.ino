// Copyright (c) 2025 David Such
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

#include <PololuMaestro.h>

// Servo channel definitions
#define WAIST       0
#define SHOULDER    1
#define ELBOW       2
#define WRIST_PITCH 3
#define WRIST_ROLL  4
#define GRIPPER     5

#ifdef SERIAL_PORT_HARDWARE_OPEN
  #define maestroSerial SERIAL_PORT_HARDWARE_OPEN
#else
  #include <AltSoftSerial.h>
  AltSoftSerial maestroSerial;
#endif

MicroMaestro servoController(maestroSerial);

void setup() {
  maestroSerial.begin(9600);

  // Configure all channels to move slowly and smoothly.
  for (uint8_t i = 0; i < 6; i++) {
    servoController.setSpeed(i, 5);
    servoController.setAcceleration(i, 127);
  }

  servoController.setTarget(SHOULDER, 3200);
  delay(2000);
  servoController.setTarget(WAIST, 6000);
  delay(2000);
  servoController.setTarget(WRIST_PITCH, 4600);
  delay(2000);
  servoController.setTarget(WRIST_ROLL, 6000);
  delay(2000);
  servoController.setTarget(GRIPPER, 3200);
  delay(2000);
  servoController.setTarget(ELBOW, 5000);
  delay(2000);
}

void loop() { }