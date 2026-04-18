/******************************************************************
  @file       static_angle_LSM9DS1_AL.ino
  @brief      Samples LSM9DS1 IMU data using Arduino library. 
  @author     David Such
  @copyright  Please see the accompanying LICENSE file.

  Code:        David Such
  Version:     1.0.0

******************************************************************/


#include <Arduino_LSM9DS1.h>

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
  // Initialize Serial Monitor
  Serial.begin(115200);
  while (!Serial);

  Serial.println("Initializing LSM9DS1 IMU...");
  
  // Initialize the IMU
  if (!IMU.begin()) {
    Serial.println("Failed to initialize LSM9DS1. Check your wiring!");
    while (1);
  }

  // FS  Full Scale - range 0:±2g | 1:±24g | 2: ±4g | 3: ±8g  (default=2)
  // ODR Output Data Rate - range 0:off | 1:10Hz | 2:50Hz | 3:119Hz | 4:238Hz | 5:476Hz, (default=3)
  IMU.setAccelFS(2);            
  IMU.setAccelODR(3);
  IMU.accelUnit = GRAVITY;

  Serial.println("LSM9DS1 Initialized!");
  Serial.println("Place the IMU in a stable position at 0 degrees to calibrate.");
  Serial.println("Press any key and hit Enter in the Serial Monitor to calibrate.");
  
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
    float ax, ay, az;

    if (IMU.accelAvailable()) {  
      IMU.readAccel(ax, ay, az); 
    }

    sumAx += ax;
    sumAy += ay;
    sumAz += 1 - az;

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
    float x, y, z;
    
    IMU.readAccel(x, y, z); 

    float ax = x - axOffset;
    float ay = y - ayOffset;
    float az = z - azOffset;

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