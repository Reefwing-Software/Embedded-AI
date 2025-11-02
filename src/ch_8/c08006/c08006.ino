/******************************************************************
  @file       c08006.ino
  @brief      LSM9DS1 tilt compensated yaw
  @author     David Such
  @copyright  Please see the accompanying LICENSE file

  Code:        David Such
  Version:     1.0.0
  Date:        25/08/24

  1.0.0     Original Release.       25/08/24

******************************************************************/

#include <ReefwingLSM9DS1.h>

ReefwingLSM9DS1 imu;

#define RAD_TO_DEG             57.295779513082320876798154814105
#define MAG_DECLINATION_SYDNEY 12.717 // MAGNETIC DECLINATION IN SYDNEY (DECIMAL)

unsigned long loopFrequency = 0;
const long displayPeriod = 1000;
unsigned long previousMillis = 0;

float roll=0, pitch=0, yaw=0;

void setup() {
  // Initialise the LSM9DS1 IMU
  imu.begin();

  //  Start Serial and wait for connection
  Serial.begin(115200);
  while (!Serial);

  if (imu.connected()) {
    imu.start();
    imu.calibrateAccel();
    imu.calibrateMag();
    delay(20);
    //  Flush first reading
    imu.readAccel();
    imu.readMag();
  } else {
    Serial.println("LSM9DS1 IMU Not Detected.");
    while(1);
  }

  Serial.println("LSM9DS1 IMU Connected."); 
  Serial.println("\nDefault Magnetometer Configuration used:");
  Serial.println("  - Full Scale: ± 4 Gauss");
  Serial.println("  - Sample Rate (ODR): 10 Hz\n");
}

void loop() {
  //  Refresh sensor data
  imu.updateSensorData();

  //  Three Axis Accelerometer Pitch and Roll in Radians
  roll = atan2(imu.data.ay, sqrt(imu.data.ax * imu.data.ax + imu.data.az * imu.data.az));
  pitch = atan2(imu.data.ax, sqrt(imu.data.ay * imu.data.ay + imu.data.az * imu.data.az));

  //  Compensate for tilt
  float mag_x_compensated = imu.data.mx * cos(pitch) + imu.data.mz * sin(pitch);
  float mag_y_compensated = imu.data.mx * sin(roll) * sin(pitch) + imu.data.my * cos(roll) - imu.data.mz * sin(roll) * cos(pitch);

  yaw = atan2(mag_y_compensated, mag_x_compensated) * RAD_TO_DEG;
  yaw -= MAG_DECLINATION_SYDNEY;

  // Normalize yaw to 0-360 degrees
  if (yaw < 0) {
    yaw += 360;
  }

  loopFrequency++;

  if (millis() - previousMillis >= displayPeriod) {
    //  Display sensor data every displayPeriod, non-blocking.
    Serial.print("Roll: "); Serial.print(roll);
    Serial.print("\tPitch: "); Serial.print(pitch);
    Serial.print("\tYaw: "); Serial.print(yaw);
  
    Serial.print("\tLoop Frequency: ");
    Serial.print(loopFrequency);
    Serial.println(" Hz");

    loopFrequency = 0;
    previousMillis = millis();
  }
}
