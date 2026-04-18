/******************************************************************
  @file       static_filter_test.ino
  @brief      Test pitch and roll for static angles
  @author     David Such
  @copyright  Please see the accompanying LICENSE file.

  Code:        David Such
  Version:     1.0.0

******************************************************************/

#include <ReefwingAHRS.h>

// Include pitch and roll data for BMI270
const float bmi270_pitch_data[][4] = {
  { -80, -0.9992, 0.0249, 0.2067 },
  { -60, -0.8727, 0.0208, 0.5320 },
  { -40, -0.6475, 0.0151, 0.7905 },
  { -20, -0.3443, 0.0042, 0.9600 },
  { 0, -0.0002, 0.0003, 1.0145 },
  { 20, 0.3389, -0.0068, 0.9459 },
  { 40, 0.6318, -0.0093, 0.7674 },
  { 60, 0.8467, -0.0077, 0.4993 },
  { 80, 0.9582, 0.0036, 0.1680 }
};
const float bmi270_roll_data[][4] = {
  { -80, 0.0032, 1.0318, 0.2240 },
  { -60, 0.0049, 0.8917, 0.5452 },
  { -40, 0.0079, 0.6491, 0.8006 },
  { -20, 0.0013, 0.3391, 0.9521 },
  { 0, 0.0004, 0.0000, 0.9878 },
  { 20, -0.0030, -0.3364, 0.9040 },
  { 40, -0.0044, -0.6141, 0.7170 },
  { 60, -0.0038, -0.8210, 0.4346 },
  { 80, 0.0078, -0.9176, 0.1025 }
};

// Include pitch and roll data for LSM9DS1
const float lsm9ds1_pitch_data[][4] = {
  { -80, -1.0018, 0.0106, 0.1963 },
  { -60, -0.8756, 0.0097, 0.5233 },
  { -40, -0.6476, 0.0058, 0.7870 },
  { -20, -0.3407, 0.0029, 0.9560 },
  { 0, 0.0000, -0.0001, 1.0054 },
  { 20, 0.3385, -0.0022, 0.9380 },
  { 40, 0.6289, -0.0001, 0.7577 },
  { 60, 0.8456, 0.0088, 0.4819 },
  { 80, 0.9585, 0.0175, 0.1559 }
};
const float lsm9ds1_roll_data[][4] = {
  { -80, 0.0024, 1.0083, 0.1552 },
  { -60, 0.0070, 0.8812, 0.4810 },
  { -40, 0.0039, 0.6490, 0.7446 },
  { -20, 0.0043, 0.3461, 0.9088 },
  { 0, -0.0004, 0.0002, 0.9594 },
  { 20, 0.0050, -0.3417, 0.8869 },
  { 40, 0.0116, -0.6396, 0.7038 },
  { 60, 0.0212, -0.8539, 0.4386 },
  { 80, 0.0325, -0.9693, 0.0997 }
};

// Include pitch and roll data for MPU6050
const float mpu6050_pitch_data[][4] = {
  { -80, 0.1162, 1.0005, 0.2898 },
  { -60, 0.0860, 0.8612, 0.6182 },
  { -40, 0.0528, 0.6399, 0.8579 },
  { -20, 0.0273, 0.3321, 1.0218 },
  { 0, -0.0013, 0.0046, 1.0700 },
  { 20, -0.0010, -0.3329, 1.0043 },
  { 40, -0.0206, -0.6297, 0.8209 },
  { 60, -0.0019, -0.8522, 0.5451 },
  { 80, 0.0362, -0.9669, 0.2246 }
};
const float mpu6050_roll_data[][4] = {
  { -80, 0.9296, 0.0737, 0.2613 },
  { -60, 0.5967, 0.0433, 0.8346 },
  { -40, 0.4992, -0.0193, 0.9051 },
  { -20, 0.2747, -0.0476, 1.0101 },
  { 0, 0.0500, -0.0262, 1.0572 },
  { 20, -0.2704, -0.0134, 1.0381 },
  { 40, -0.5765, 0.0084, 0.9045 },
  { 60, -0.8237, 0.0360, 0.6829 },
  { 80, -0.9813, 0.0665, 0.3878 }
};

// Instantiate Reefwing AHRS and data
ReefwingAHRS ahrs;
SensorData staticData;

void testFilter(SensorFusion filter, const char* sensorName, const char* dataType, const float data[][4], int dataSize) {
  ahrs.reset();
  ahrs.setFusionAlgorithm(filter);
  ahrs.setDOF(DOF::DOF_6);

  Serial.print("\nSensor: ");
  Serial.println(sensorName);
  Serial.print("Type: ");
  Serial.println(dataType);
  Serial.println("Angle, Calculated Roll, Calculated Pitch");

  for (int i = 0; i < dataSize; i++) {
    staticData.ax = data[i][1];
    staticData.ay = data[i][2];
    staticData.az = data[i][3];

    // Update the AHRS with static accelerometer data and zero gyroscope and magnetometer
    ahrs.setData(staticData);
    ahrs.update();

    // Output the results
    Serial.print(data[i][0]);  // Angle
    Serial.print(", ");
    Serial.print(ahrs.angles.roll, 2);  // Calculated Roll
    Serial.print(", ");
    Serial.println(ahrs.angles.pitch, 2);  // Calculated Pitch
  }
}

void setup() {
  Serial.begin(115200);
  while (!Serial);

  // Set gyroscope data to zero (static test)
  staticData.gx = 0.0f;
  staticData.gy = 0.0f;
  staticData.gz = 0.0f;

  // Set magnetometer data to zero (not used in DOF::DOF_6)
  staticData.mx = 0.0f;
  staticData.my = 0.0f;
  staticData.mz = 0.0f;

  Serial.println("Testing Reefwing AHRS Library with Static IMU Data using Complementary Filter\n");
  ahrs.begin();

  // Set the complementary filter
  ahrs.setFusionAlgorithm(SensorFusion::COMPLEMENTARY);
  ahrs.setAlpha(0.0f); // Set alpha to 0 to ignore gyro contribution

  // Test complementary filter with each sensor dataset
  testFilter(SensorFusion::COMPLEMENTARY, "BMI270", "Pitch", bmi270_pitch_data, sizeof(bmi270_pitch_data) / sizeof(bmi270_pitch_data[0]));
  testFilter(SensorFusion::COMPLEMENTARY, "BMI270", "Roll", bmi270_roll_data, sizeof(bmi270_roll_data) / sizeof(bmi270_roll_data[0]));
  testFilter(SensorFusion::COMPLEMENTARY, "LSM9DS1", "Pitch", lsm9ds1_pitch_data, sizeof(lsm9ds1_pitch_data) / sizeof(lsm9ds1_pitch_data[0]));
  testFilter(SensorFusion::COMPLEMENTARY, "LSM9DS1", "Roll", lsm9ds1_roll_data, sizeof(lsm9ds1_roll_data) / sizeof(lsm9ds1_roll_data[0]));
  testFilter(SensorFusion::COMPLEMENTARY, "MPU6050", "Pitch", mpu6050_pitch_data, sizeof(mpu6050_pitch_data) / sizeof(mpu6050_pitch_data[0]));
  testFilter(SensorFusion::COMPLEMENTARY, "MPU6050", "Roll", mpu6050_roll_data, sizeof(mpu6050_roll_data) / sizeof(mpu6050_roll_data[0]));
}

void loop() { }
