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

// Pin Definitions
#define RX_PIN  8
#define TX_PIN  9
#define RST_PIN 2

#ifdef SERIAL_PORT_HARDWARE_OPEN
  #define maestroSerial SERIAL_PORT_HARDWARE_OPEN
#else
  #include <AltSoftSerial.h>
  AltSoftSerial maestroSerial;
#endif

MicroMaestro servoController(maestroSerial);

void setup() {
  pinMode(RST_PIN, OUTPUT);     // Configure pin 2 as an output
  digitalWrite(RST_PIN, HIGH);  // Set it inactive (not resetting)

  Serial.begin(115200);
  Serial.println("6-DOF Robot Arm Test");
  maestroSerial.begin(9600);
  maestroSerial.println("reset"); // Establishes connection
  Serial.println("Servo controller connected.");

  uint16_t errors = servoController.getErrors();
  uint8_t status = servoController.getScriptStatus();

  Serial.print("Error Code: ");
  Serial.println(errors);

  // 1 if script is stopped, 0 if running.
  if (status) {
    Serial.println("Controller script is stopped.");
  }
  else {
    Serial.println("Controller script is running.");
  }

  // Centre arm servos
  servoController.setTarget(SHOULDER, 6000);
  servoController.setTarget(ELBOW, 6000);
  servoController.setTarget(WRIST_PITCH, 6000);
  servoController.setTarget(WRIST_ROLL, 6000);
  servoController.setTarget(GRIPPER, 6000);
  delay(2000);

  for (uint8_t i = 0; i < 6; i++) {
    uint16_t position = servoController.getPosition(i);
    Serial.print("Channel: ");
    Serial.print(i);
    Serial.print(" Position: ");
    Serial.println(position);
  }
}

void loop() { }