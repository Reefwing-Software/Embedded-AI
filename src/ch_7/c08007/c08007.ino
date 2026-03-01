/******************************************************************
  @file       c08007.ino
  @brief      LSM9DS1 simple dead reckoning example
  @author     David Such
  @copyright  Please see the accompanying LICENSE file

  Code:        David Such
  Version:     1.0.0
  Date:        25/08/24

  1.0.0     Original Release.       25/08/24

******************************************************************/

#include <ReefwingLSM9DS1.h>

ReefwingLSM9DS1 imu;

unsigned long loopFrequency = 0;
const long displayPeriod = 1000;
unsigned long previousMillis = 0;
unsigned long previousTime = 0;

// Current acceleration in ms-2
float ax, ay, az;

// Velocity and position
float vx = 0, vy = 0, vz = 0;
float px = 0, py = 0, pz = 0;

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
  } else {
    Serial.println("LSM9DS1 IMU Not Detected.");
    while(1);
  }

  Serial.println("LSM9DS1 IMU Connected."); 
}

void loop() {
  //  Refresh sensor data
  imu.updateSensorData();

  // Convert the acceleration values from g's to m/s^2
  ax = imu.data.ax * 9.81;
  ay = imu.data.ay * 9.81;
  az = imu.data.az * 9.81;

  // Correct the z-axis for gravity
  az -= 9.81;

  // Calculate time elapsed
  unsigned long currentTime = millis();
  float deltaTime = (currentTime - previousTime) / 1000.0; // Convert to seconds
  previousTime = currentTime;

  // Integrate acceleration to get velocity
  vx += ax * deltaTime;
  vy += ay * deltaTime;
  vz += az * deltaTime;

  // Integrate velocity to get position
  px += vx * deltaTime;
  py += vy * deltaTime;
  pz += vz * deltaTime;

  loopFrequency++;

  if (millis() - previousMillis >= displayPeriod) {
    Serial.print("Position: X=");
    Serial.print(px);
    Serial.print(" m, Y=");
    Serial.print(py);
    Serial.print(" m, Z=");
    Serial.println(pz);
    Serial.print("Velocity: X=");
    Serial.print(vx);
    Serial.print(" m/s, Y=");
    Serial.print(vy);
    Serial.print(" m/s, Z=");
    Serial.println(vz);

    Serial.print("\tLoop Frequency: ");
    Serial.print(loopFrequency);
    Serial.println(" Hz");

    loopFrequency = 0;
    previousMillis = millis();
  }

}
