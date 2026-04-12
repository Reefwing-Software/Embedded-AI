/******************************************************************
  @file       c07003.ino
  @brief      LSM9DS1 Accelerometer single axis vs two axis
  @author     David Such
  @copyright  Please see the accompanying LICENSE file

  Code:        David Such
  Version:     1.0.0

******************************************************************/

#include <ReefwingLSM9DS1.h>

ReefwingLSM9DS1 imu;

#define RAD_TO_DEG        57.295779513082320876798154814105

const long displayPeriod = 1000;
unsigned long previousMillis = 0;
ScaledData acc;

void setup() {
  // Initialise the LSM9DS1 IMU
  imu.begin();

  //  Start Serial and wait for connection
  Serial.begin(115200);
  while (!Serial);

  if (imu.connected()) { 
    imu.start();
    imu.calibrateAccel();
    delay(20);
    //  Flush first reading
    imu.readAccel();
  } 
  else {
    Serial.println("LSM9DS1 IMU Not Detected.");
    while(1);
  }

  Serial.println("LSM9DS1 IMU Connected.");
  Serial.println("\nDefault Accelerometer Configuration used:");
  Serial.println("  - Full Scale: ± 8 g");
  Serial.println("  - Sample Rate (ODR): 119 Hz\n");
}

void loop() {
  //  Read Accelerometer
  if (imu.accelAvailable()) {
    acc = imu.readAccel();
  
    if (millis() - previousMillis >= displayPeriod) {
      //  Single Axis Pitch and Roll in Degrees
      float single_axis_roll = asin(acc.sy) * RAD_TO_DEG;
      float single_axis_pitch = asin(acc.sx) * RAD_TO_DEG;
      Serial.print("Roll-1: "); Serial.print(single_axis_roll);
      Serial.print("\tPitch-1: "); Serial.println(single_axis_pitch);

      //  Two Axis Pitch and Roll in Degrees
      float two_axis_roll = atan(acc.sy/acc.sz) * RAD_TO_DEG;
      float two_axis_pitch = atan(acc.sx/acc.sz) * RAD_TO_DEG;
      Serial.print("Roll-2: "); Serial.print(two_axis_roll);
      Serial.print("\tPitch-2: "); Serial.println(two_axis_pitch);

      previousMillis = millis();
    }
  }
}
