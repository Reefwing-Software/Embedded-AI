/******************************************************************
  @file       gyro_test.ino
  @brief      LSM9DS1 gyro roll, pitch, and yaw test
  @author     David Such
  @copyright  Please see the accompanying LICENSE file

  Code:        David Such
  Version:     1.0.0
  Date:        25/08/24

  1.0.0     Original Release.       25/08/24

******************************************************************/

#include <ReefwingLSM9DS1.h>

ReefwingLSM9DS1 imu;

#define RAD_TO_DEG        57.295779513082320876798154814105
#define DEG_TO_RAD        0.017453292519943295769236907684886

const long displayPeriod = 1000;  // Display period in milliseconds
unsigned long previousMillis = 0;
unsigned long lastUpdate = 0;  // Time of the last update
unsigned long lastSampleTime = 0; // Time of the last sensor sample
const int sampleInterval = 10;  // 100 Hz sampling interval (10 ms)

float roll = 0.0, pitch = 0.0, yaw = 0.0;

void setup() {
  // Initialise the LSM9DS1 IMU
  imu.begin();

  // Start Serial and wait for connection
  Serial.begin(115200);
  while (!Serial);

  if (imu.connected()) { 
    imu.start();
    imu.calibrateGyro();
    imu.calibrateAccel();
    delay(20);
    // Flush first reading
    imu.readGyro();
    imu.readAccel();
  } 
  else {
    Serial.println("LSM9DS1 IMU Not Detected.");
    while(1);
  }

  Serial.println("LSM9DS1 IMU Connected.");
  Serial.println("\nDefault Gyro Configuration used:");
  Serial.println("  - Full Scale: 2000 DPS");
  Serial.println("  - Sample Rate (ODR): 119 Hz\n");

  lastUpdate = millis();
  lastSampleTime = millis();
}

void loop() {
  unsigned long currentMillis = millis();

  // Check if it's time to sample the sensors (100 Hz = 10 ms intervals)
  if (currentMillis - lastSampleTime >= sampleInterval) {
    lastSampleTime = currentMillis;
    
    imu.updateSensorData();

    float deltaTime = (currentMillis - lastUpdate) / 1000.0;  // Calculate delta time in seconds
    lastUpdate = currentMillis;

    // Convert roll, pitch, and yaw to radians
    float rollRad = roll * DEG_TO_RAD;
    float pitchRad = pitch * DEG_TO_RAD;

    // Convert Gyro Data from DPS to rad/s
    float p = imu.data.gx * DEG_TO_RAD;  // Roll rate (rad/s)
    float q = imu.data.gy * DEG_TO_RAD;  // Pitch rate (rad/s)
    float r = imu.data.gz * DEG_TO_RAD;  // Yaw rate (rad/s)

    // Calculate the Euler rates using the gyroscope data
    float rollRate = p + sin(rollRad) * tan(pitchRad) * q + cos(rollRad) * tan(pitchRad) * r;
    float pitchRate = cos(rollRad) * q - sin(rollRad) * r;
    float yawRate = (sin(rollRad) / cos(pitchRad)) * q + (cos(rollRad) / cos(pitchRad)) * r;

    // Integrate the Euler rates to get the Euler angles
    roll += rollRate * deltaTime * RAD_TO_DEG;
    pitch += pitchRate * deltaTime * RAD_TO_DEG;
    yaw += yawRate * deltaTime * RAD_TO_DEG;
  }

  // Display results every second (1000 ms)
  if (currentMillis - previousMillis >= displayPeriod) {
    Serial.print("Roll: "); Serial.print(roll);
    Serial.print("\tPitch: "); Serial.print(pitch);
    Serial.print("\tYaw: "); Serial.print(yaw);

    Serial.print("\tSample Rate: ");
    Serial.print(1000.0 / sampleInterval);  // Should be close to 50 Hz
    Serial.println(" Hz");

    previousMillis = millis();
  }
}
