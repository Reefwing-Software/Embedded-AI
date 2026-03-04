// Copyright (c) 2025 David Such
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

// Sketch c09004.ino
// Build Step 2: Create Movement Routines
// The Nominal Sample

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
#define LED_PIN 13

// Pick and Place Repetitions
#define REPS 3
#define MAX_COUNT 10  // maximum blinks/sec

#ifdef SERIAL_PORT_HARDWARE_OPEN
  #define maestroSerial SERIAL_PORT_HARDWARE_OPEN
#else
  #include <AltSoftSerial.h>
  AltSoftSerial maestroSerial;
#endif

// State variables for ISR
volatile bool ledState = false;
volatile bool inPausePhase = false;

volatile uint8_t count = 1; 
volatile uint16_t blinkIntervalMs = 0;
volatile uint8_t blinkTarget = 0;
volatile uint8_t blinkCount = 0;
volatile uint16_t phaseTimer = 0;

MicroMaestro servoController(maestroSerial);

void setupTimer2() {
  cli(); // Disable interrupts

  TCCR2A = 0;
  TCCR2B = 0;

  TCCR2A |= (1 << WGM21);  // CTC mode

  OCR2A = 249;             // 1 ms tick (16 MHz / 64 / 250)
  TCCR2B |= (1 << CS22);   // Prescaler 64
  TIMSK2 |= (1 << OCIE2A); // Enable compare match interrupt

  sei(); // Enable interrupts

  // Initialize blink timing
  blinkTarget = count;
  blinkIntervalMs = 1000 / (2 * blinkTarget); // half-cycle
}

ISR(TIMER2_COMPA_vect) {
  static uint16_t intervalCounter = 0;

  if (inPausePhase) {
    phaseTimer++;
    if (phaseTimer >= 1000) {
      // End of pause phase
      inPausePhase = false;
      blinkCount = 0;
      phaseTimer = 0;
    }
    return;
  }

  // Blinking phase
  if (blinkCount >= 2 * blinkTarget) {
    // End of blinking phase
    inPausePhase = true;
    ledState = false;
    digitalWrite(LED_PIN, LOW);
    return;
  }

  intervalCounter++;
  if (intervalCounter >= blinkIntervalMs) {
    intervalCounter = 0;
    ledState = !ledState;
    digitalWrite(LED_PIN, ledState);
    blinkCount++;
  }
}

void open_gripper() {
  servoController.setTarget(GRIPPER, 3200);
}

void close_gripper() {
  servoController.setTarget(GRIPPER, 5400);
}

void roll_right() {
  servoController.setTarget(WRIST_ROLL, 8200);
}

void roll_left() {
  servoController.setTarget(WRIST_ROLL, 4000);
}

void swing_right() {
  servoController.setSpeed(WAIST, 5);
  servoController.setAcceleration(WAIST, 64);
  servoController.setTarget(WAIST, 5000);
  delay(1000);
  servoController.setTarget(WAIST, 4500);
  delay(1000);
  servoController.setTarget(WAIST, 3200);
}

void swing_straight() {
  servoController.setTarget(WAIST, 6000);
  delay(1000);
}

void roll_straight() {
  servoController.setTarget(WRIST_ROLL, 6000);
}

void up() {
  servoController.setTarget(SHOULDER, 4000);
  delay(1000);
  servoController.setTarget(ELBOW, 6000);
  delay(1000);
  servoController.setTarget(WRIST_PITCH, 6000);
}

void down() {
  servoController.setTarget(SHOULDER, 3200);
  delay(1000);
  servoController.setTarget(ELBOW, 8000);
  delay(1000);
}

void forward() {
  servoController.setTarget(SHOULDER, 3200);
  delay(1000);
  servoController.setTarget(WRIST_PITCH, 4000);
  servoController.setTarget(ELBOW, 8500);
  delay(2000);
}

void start() {
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
  pinMode(LED_PIN, OUTPUT);
  setupTimer2();

  Serial.begin(115200);
  Serial.println("6-DOF Robot Arm Test");
  maestroSerial.begin(9600);

  uint16_t errors = servoController.getErrors();

  Serial.println("Servo controller connected.");
  Serial.print("Error Code: ");
  Serial.println(errors);

  // Configure all channels to move slowly and smoothly.
  for (uint8_t i = 0; i < 6; i++) {
    servoController.setSpeed(i, 5);
    servoController.setAcceleration(i, 127);
  }
  start();
}

void loop() {
  static bool done = false;

  if (count < REPS + 1) {
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
    cli();
    blinkTarget = count;
    blinkIntervalMs = 1000 / (2 * blinkTarget);
    sei();
  } else if (!done) {
    start();
    cli();
    blinkTarget = MAX_COUNT;
    blinkIntervalMs = 1000 / (2 * blinkTarget);
    sei();
    done = true;
  }
}