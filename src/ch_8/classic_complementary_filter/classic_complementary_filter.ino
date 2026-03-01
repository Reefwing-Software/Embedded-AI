#include <ReefwingAHRS.h>
#include <Arduino_BMI270_BMM150.h> // Includes the library for the IMU sensors on the Nano 33 BLE Sense Rev. 2

// Create an instance of the ReefwingAHRS class
ReefwingAHRS ahrs;
SensorData data;

// Display and loop frequency variables
int loopFrequency = 0;
const long displayPeriod = 1000; // Display updates every 1000 ms
unsigned long previousMillis = 0;

// Timer variables for IMU reading at a fixed frequency
const int imuFrequency = 50; // IMU update frequency in Hz
const long imuInterval = 1000 / imuFrequency; // Interval in milliseconds
unsigned long lastIMUUpdate = 0;

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
  while (!Serial); // Wait for the serial monitor to connect

  // Initialize the AHRS library
  ahrs.begin();
  ahrs.setFusionAlgorithm(SensorFusion::CLASSIC);  // Set the complementary filter algorithm
  ahrs.setAlpha(0.95);                             // Set the filter coefficient (alpha)
  ahrs.setDeclination(12.717);                     // Set the magnetic declination for Sydney, Australia

  // Print board and sensor information
  Serial.println("Initializing Reefwing AHRS...");
  Serial.print("Detected Board - ");
  Serial.println(ahrs.getBoardTypeString());

  if (IMU.begin() && ahrs.getBoardType() == BoardType::NANO33BLE_SENSE_R2) {
    Serial.println("BMI270 & BMM150 IMUs Connected.");
    Serial.print("Gyroscope sample rate: ");
    Serial.print(IMU.gyroscopeSampleRate());
    Serial.println(" Hz");
    Serial.print("Accelerometer sample rate: ");
    Serial.print(IMU.accelerationSampleRate());
    Serial.println(" Hz");
    Serial.print("Magnetic field sample rate: ");
    Serial.print(IMU.magneticFieldSampleRate());
    Serial.println(" Hz");
    Serial.println("Initialization complete.\n");
  } else {
    Serial.println("BMI270 & BMM150 IMUs Not Detected. Check connections.");
    while (1); // Halt the program if sensors are not detected
  }
}

void loop() {
  unsigned long currentMillis = millis();

  // Read IMU data at a fixed frequency (e.g., 50 Hz)
  if (currentMillis - lastIMUUpdate >= imuInterval) {
    lastIMUUpdate = currentMillis;

    // Read data from the IMU sensors
    if (IMU.gyroscopeAvailable()) {
      IMU.readGyroscope(data.gx, data.gy, data.gz); // Gyroscope data (degrees/sec)
    } else {
      Serial.println("Error: Gyroscope data unavailable.");
    }

    if (IMU.accelerationAvailable()) {
      IMU.readAcceleration(data.ax, data.ay, data.az); // Accelerometer data (g's)
    } else {
      Serial.println("Error: Accelerometer data unavailable.");
    }

    if (IMU.magneticFieldAvailable()) {
      IMU.readMagneticField(data.mx, data.my, data.mz); // Magnetometer data (microteslas)
    } 

    // Set the sensor data in the AHRS library and update the filter
    ahrs.setData(data);
    ahrs.update();
  }

  // Display the angles and loop frequency every `displayPeriod` milliseconds
  if (currentMillis - previousMillis >= displayPeriod) {
    // Print raw sensor data for debugging
    Serial.print("Gyroscope: gx = ");
    Serial.print(data.gx, 4);
    Serial.print(", gy = ");
    Serial.print(data.gy, 4);
    Serial.print(", gz = ");
    Serial.println(data.gz, 4);

    Serial.print("Accelerometer: ax = ");
    Serial.print(data.ax, 4);
    Serial.print(", ay = ");
    Serial.print(data.ay, 4);
    Serial.print(", az = ");
    Serial.println(data.az, 4);

    Serial.print("Magnetometer: mx = ");
    Serial.print(data.mx, 4);
    Serial.print(", my = ");
    Serial.print(data.my, 4);
    Serial.print(", mz = ");
    Serial.println(data.mz, 4);
    
    Serial.print("--> Roll: ");
    Serial.print(ahrs.angles.roll, 2);  // Roll angle (degrees)
    Serial.print("\tPitch: ");
    Serial.print(ahrs.angles.pitch, 2); // Pitch angle (degrees)
    Serial.print("\tYaw: ");
    Serial.print(ahrs.angles.yaw, 2);   // Yaw angle (degrees)
    Serial.print("\tHeading: ");
    Serial.print(ahrs.angles.heading, 2); // Corrected heading (degrees)
    Serial.print("\tLoop Frequency: ");
    Serial.print(loopFrequency);
    Serial.println(" Hz");

    // Reset loop frequency counter and update the timestamp
    loopFrequency = 0;
    previousMillis = currentMillis;
  }

  // Increment loop frequency counter
  loopFrequency++;
}