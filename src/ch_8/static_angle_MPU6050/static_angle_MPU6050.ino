/******************************************************************
  @file       static_angle_MPU6050.ino
  @brief      Samples MPU-6050 IMU data using Reefwing library. 
  @author     David Such
  @copyright  Please see the accompanying LICENSE file.

  Code:        David Such
  Version:     1.0.0
  Date:        25/11/24

  1.0.0 Original Release.                         25/11/24

******************************************************************/

#include <ReefwingMPU6050.h>

ReefwingMPU6050 imu;

// Calibration offset values (adjust as needed after calibration)
float axOffset = 0.0;
float ayOffset = 0.0;
float azOffset = 0.0;

// Angle configurations
const int numAngles = 9; // Angles from -80° to +80° in steps of 20°
int angles[numAngles] = {0, 20, 40, 60, 80, -20, -40, -60, -80};

// Sample configuration
const int numSamples = 10; // Number of samples per angle

void setup() {
  imu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G);

  // Initialize Serial Monitor
  Serial.begin(115200);
  while (!Serial);

  if (imu.connected()) {
    Serial.println("Initializing MPU-6050 IMU...");
  } 
  else {
    Serial.println("Failed to initialize MPU-6050.");
    while(1);
  }

  // Accelerometer default range is ±2 g
  // Accelerometer default output data rate is 1 kHz.

  Serial.println("MPU-6050 Initialized!");
  Serial.println("Place the IMU in a stable position at 0 degrees to calibrate.");
  Serial.println("Press Enter in the Serial Monitor to calibrate.");
  
  while (!Serial.available());
  Serial.read(); // Clear the input buffer

  // Perform calibration at 0 degrees
  calibrateIMU();
  Serial.println("Calibration complete.");
  Serial.println("Starting angle measurements...");
}

void loop() {
  for (int i = 0; i < numAngles; i++) {
    int currentAngle = angles[i];

    Serial.print("Position the IMU at ");
    Serial.print(currentAngle);
    Serial.println(" degrees. Hit Enter to proceed.");
    while (!Serial.available());
    Serial.read(); // Wait for user input to proceed

    Serial.println("Collecting data...");
    collectDataForAngle(currentAngle);
    Serial.println("Data collection complete.");
  }

  Serial.println("All angle measurements complete!");
  while (1); // Stop further execution
}

void calibrateIMU() {
  float sumAx = 0.0, sumAy = 0.0, sumAz = 0.0;

  for (int i = 0; i < numSamples; i++) {
    imu.updateSensorData();

    sumAx += imu.data.ax;
    sumAy += imu.data.ay;
    sumAz += 1 - imu.data.az;

    delay(100); // Delay between samples
  }

  axOffset = sumAx / numSamples;
  ayOffset = sumAy / numSamples;
  azOffset = sumAz / numSamples;

  Serial.print("Offsets: ");
  Serial.print("ax: ");
  Serial.print(axOffset, 3);
  Serial.print(", ay: ");
  Serial.print(ayOffset, 3);
  Serial.print(", az: ");
  Serial.println(azOffset, 3);
}

void collectDataForAngle(int angle) {
  Serial.println("Angle (degrees), ax (m/s^2), ay (m/s^2), az (m/s^2)");

  for (int i = 0; i < numSamples; i++) {
    imu.updateSensorData();

    float ax = imu.data.ax - axOffset;
    float ay = imu.data.ay - ayOffset;
    float az = imu.data.az - azOffset;

    Serial.print(angle);
    Serial.print(",");
    Serial.print(ax, 3);
    Serial.print(",");
    Serial.print(ay, 3);
    Serial.print(",");
    Serial.println(az, 3);

    delay(100); // Delay between samples - min = 8 ms for 119 Hz ODR
  }
}
