// Copyright (c) 2026 David Such
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

// Sketch c09001.ino
// Why you don't use the SoftwareSerial library explanation

#include <AltSoftSerial.h>

// AltSoftSerial always uses these pins:
//
// Board          Transmit  Receive   PWM Unusable
// -----          --------  -------   ------------
// Arduino Uno        9         8         10

AltSoftSerial altSerial;

void setup() {
  Serial.begin(9600);
  while (!Serial) ; // wait for Arduino Serial Monitor to open
  Serial.println("AltSoftSerial Test Begin");
  altSerial.begin(9600);
  altSerial.println("Hello World");
}

void loop() {
  char c;

  if (Serial.available()) {
    c = Serial.read();
    altSerial.print(c);
  }
  if (altSerial.available()) {
    c = altSerial.read();
    Serial.print(c);
  }
}