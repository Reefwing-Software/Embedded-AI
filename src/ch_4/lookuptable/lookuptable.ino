/******************************************************************
  @file       lookuptable.ino
  @brief      Battery SOC lookuptable - normalised for ML comparison
  @author     David Such
  @copyright  Please see the accompanying LICENSE file.

  Code:        David Such
  Version:     1.0.0
  Date:        07/12/24

  1.0.0 Original Release.                         07/12/24

******************************************************************/

#define SOC_TABLE_SIZE 21
#define SCALE_FACTOR 1000000  // Scaling factor for values

typedef struct {
    int32_t v_scaled; // Scaled voltage (0 to SCALE_FACTOR)
    int32_t soc_scaled; // Scaled state of charge (0 to SCALE_FACTOR)
} soc_lookup_t;

soc_lookup_t capacity[SOC_TABLE_SIZE] = {
    {982, 0},   {1098, 5},   {1106, 10},  {1112, 15},  {1118, 20},  {1124, 25},  {1128, 30},
    {1136, 35}, {1139, 40},  {1146, 45},  {1151, 50},  {1156, 55},  {1163, 60},  {1174, 65},
    {1186, 70}, {1196, 75},  {1207, 80},  {1225, 85},  {1233, 90},  {1245, 95},  {1260, 100}
};

// Provided test data
const int32_t voltage_soc[100][2] = {
    {1250, 100}, {1238, 96}, {1232, 94}, {1220, 92}, {1223, 89},
    {1225, 87}, {1215, 85}, {1220, 82}, {1205, 80}, {1203, 78},
    {1201, 74}, {1199, 72}, {1174, 70}, {1197, 67}, {1180, 65},
    {1167, 62}, {1169, 59}, {1169, 57}, {1152, 53}, {1152, 51},
    {1149, 49}, {1126, 46}, {1140, 43}, {1141, 41}, {1133, 37},
    {1127, 35}, {1123, 33}, {1113, 29}, {1104, 26}, {1073, 24},
    {1091, 21}, {1086, 18}, {1034, 15}, {1059, 13}, {1145, 24},
    {1162, 35}, {1185, 49}, {1214, 63}, {1243, 77}, {1253, 89},
    {1253, 94}, {1253, 97}, {1253, 99}, {1253, 99}, {1253, 100},
    {1252, 100}, {1252, 100}, {1251, 100}, {1251, 100}, {1251, 100},
    {1251, 100}, {1251, 100}, {1242, 98}, {1226, 93}, {1238, 89},
    {1213, 86}, {1213, 81}, {1208, 77}, {1202, 74}, {1192, 69},
    {1173, 64}, {1196, 61}, {1166, 56}, {1144, 51}, {1141, 48},
    {1129, 43}, {1135, 38}, {1130, 35}, {1119, 29}, {1109, 23},
    {1075, 20}, {1057, 14}, {1061, 13}, {1137, 20}, {1162, 35},
    {1178, 46}, {1207, 60}, {1236, 74}, {1253, 87}, {1253, 94},
    {1253, 97}, {1253, 99}, {1253, 99}, {1253, 100}, {1252, 100},
    {1252, 100}, {1251, 100}, {1251, 100}, {1251, 100}, {1251, 100},
    {1251, 100}, {1238, 97}, {1225, 86}, {1199, 73}, {1146, 61},
    {1128, 54}, {1082, 40}, {1117, 28}, {1059, 13}, {1064, 13}
};

// Interpolation function using scaled values
int32_t interpolate(soc_lookup_t *capacity, int32_t charge_scaled) {
    // Constrain charge to the min and max scaled values
    charge_scaled = constrain(charge_scaled, capacity[0].v_scaled, capacity[SOC_TABLE_SIZE - 1].v_scaled);

    // Interpolate the scaled SoC value
    for (int i = 0; i < SOC_TABLE_SIZE - 1; i++) {
        if (capacity[i].v_scaled <= charge_scaled && capacity[i + 1].v_scaled >= charge_scaled) {
            int32_t diffx = charge_scaled - capacity[i].v_scaled;
            int32_t diffn = capacity[i + 1].v_scaled - capacity[i].v_scaled;

            return capacity[i].soc_scaled + (capacity[i + 1].soc_scaled - capacity[i].soc_scaled) * diffx / diffn;
        }
    }

    return 0; // Not in Range
}

// Calculate RMSE, MAE, and print results
void calculateErrors() {
    int32_t total_squared_error = 0;
    int32_t total_absolute_error = 0;

    for (int i = 0; i < 100; i++) {
        int32_t voltage = voltage_soc[i][0];
        int32_t true_soc = voltage_soc[i][1];

        // Interpolate the SOC based on the voltage
        int32_t predicted_soc = interpolate(capacity, voltage);

        // Calculate errors
        int32_t error = predicted_soc - true_soc;
        total_squared_error += error * error;
        total_absolute_error += abs(error);
    }

    // Calculate RMSE and MAE
    float rmse = sqrt(total_squared_error / 100.0);
    float mae = total_absolute_error / 100.0;

    // Print results
    Serial.print("RMSE: ");
    Serial.println(rmse);
    Serial.print("MAE: ");
    Serial.println(mae);

    int32_t total_sum_of_squares = 0;
    int32_t mean_true_soc = 0;

    // Calculate mean true SOC
    for (int i = 0; i < 100; i++) {
        mean_true_soc += voltage_soc[i][1];
    }
    mean_true_soc /= 100;

    // Calculate total sum of squares
    for (int i = 0; i < 100; i++) {
        int32_t diff = voltage_soc[i][1] - mean_true_soc;
        total_sum_of_squares += diff * diff;
    }

    // Calculate R^2
    float r_squared = 1.0 - (total_squared_error / (float)total_sum_of_squares);
    Serial.print("R^2: ");
    Serial.println(r_squared);
}

void setup() {
    Serial.begin(115200);
    while (!Serial);

    calculateErrors();
}

void loop() { }