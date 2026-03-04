// Copyright (c) 2026 David Such
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

// Sketch c09005.ino
// Build Step 2: Create Movement Routines
// The Anomaly Sample

#include <PololuMaestro.h>

#define WAIST        0
#define SHOULDER     1
#define ELBOW        2
#define WRIST_PITCH  3
#define WRIST_ROLL   4
#define GRIPPER      5

#define RX_PIN  8
#define TX_PIN  9
#define REPS    4

#ifdef SERIAL_PORT_HARDWARE_OPEN
  #define maestroSerial SERIAL_PORT_HARDWARE_OPEN
#else
  #include <AltSoftSerial.h>
  AltSoftSerial maestroSerial;
#endif

MicroMaestro servoController(maestroSerial);

bool check_for_anomaly(const char* step) {
  if (random(0, 10) < 2) { // 20% chance to simulate an anomaly
    Serial.print("⚠️  Anomaly detected at: ");
    Serial.println(step);
    while (true); // Simulate freeze (halt system)
  }
  return false;
}

void open_gripper() {
  check_for_anomaly("open_gripper");
  servoController.setTarget(GRIPPER, 3200);
}

void close_gripper() {
  check_for_anomaly("close_gripper");
  servoController.setTarget(GRIPPER, 5400);
}

void roll_right() {
  check_for_anomaly("roll_right");
  servoController.setTarget(WRIST_ROLL, 8200);
}

void roll_straight() {
  check_for_anomaly("roll_straight");
  servoController.setTarget(WRIST_ROLL, 6000);
}

void swing_right() {
  check_for_anomaly("swing_right");
  servoController.setTarget(WAIST, 5000);
  delay(1000);
  servoController.setTarget(WAIST, 4500);
  delay(1000);
  servoController.setTarget(WAIST, 3200);
}

void swing_straight() {
  check_for_anomaly("swing_straight");
  servoController.setTarget(WAIST, 6000);
  delay(1000);
}

void up() {
  check_for_anomaly("up");
  servoController.setTarget(SHOULDER, 4000);
  delay(1000);
  servoController.setTarget(ELBOW, 6000);
  delay(1000);
  servoController.setTarget(WRIST_PITCH, 6000);
}

void down() {
  check_for_anomaly("down");
  servoController.setTarget(SHOULDER, 3200);
  delay(1000);
  servoController.setTarget(ELBOW, 8000);
  delay(1000);
}

void forward() {
  check_for_anomaly("forward");
  servoController.setTarget(SHOULDER, 3200);
  delay(1000);
  servoController.setTarget(WRIST_PITCH, 4000);
  servoController.setTarget(ELBOW, 8500);
  delay(2000);
}

void start() {
  Serial.println("Resetting to home...");
  servoController.setTarget(SHOULDER, 3200);
  delay(1000);
  swing_straight();
  roll_straight();
  open_gripper();
  servoController.setTarget(ELBOW, 8000);
  delay(1000);
  servoController.goHome();
}

void setup() {
  Serial.begin(115200);
  maestroSerial.begin(9600);
  delay(1000); // Give time for serial to connect

  Serial.println("Starting 6-DOF Robot Arm with Anomaly Simulation");

  for (uint8_t i = 0; i < 6; i++) {
    servoController.setSpeed(i, 5);
    servoController.setAcceleration(i, 127);
  }

  randomSeed(analogRead(A0)); // Seed randomness
  start();
}

void loop() {
  static uint8_t count = 0;

  if (count < REPS) {
    Serial.print("Cycle ");
    Serial.print(count + 1);
    Serial.println(" starting...");

    up();
    forward();
    close_gripper();
    up();
    roll_right();
    swing_right();
    roll_straight();
    forward();
    up();
    swing_straight();
    down();

    count++;
  } else {
    Serial.println("All cycles complete. Returning to start position.");
    start();
    while (true); // End execution
  }
}