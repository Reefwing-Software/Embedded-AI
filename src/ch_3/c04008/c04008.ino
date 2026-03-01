/******************************************************************
  @file       c04008.ino
  @brief      Battery SOC lookuptable - 3S
  @author     David Such
  @copyright  Please see the accompanying LICENSE file.

  Code:        David Such
  Version:     1.0.0
  Date:        07/12/24

  1.0.0 Original Release.                         07/12/24

******************************************************************/

#define VBAT      A0                //  Analogue Pin A0

const float VLOGIC = 5.0;           //  UNO has 5V logic
const float R1 = 10000.0;           //  10K Resistor
const float R2 = 6800.0;            //  6K8 Resistor
const float RATIO = (R1 + R2) / R2; //  Voltage Divider ratio
const float SCALE = VLOGIC * RATIO; //  Voltage conversion factor

#define SOC_TABLE_SIZE 21

typedef struct {
    uint16_t v100; // voltage in hundredths of a volt
    uint16_t soc;  // state of charge percentage
} soc_lookup_t;

soc_lookup_t capacity[SOC_TABLE_SIZE] = {
    {982, 0},   {1098, 5},   {1106, 10},  {1112, 15},  {1118, 20},  {1124, 25},  {1128, 30},
    {1136, 35}, {1139, 40},  {1146, 45},  {1151, 50},  {1156, 55},  {1163, 60},  {1174, 65},
    {1186, 70}, {1196, 75},  {1207, 80},  {1225, 85},  {1233, 90},  {1245, 95},  {1260, 100}
};

uint16_t interpolate(soc_lookup_t *capacity, float charge) {
    // Use the first and last elements for min and max values
    uint16_t min_v100 = capacity[0].v100;
    uint16_t max_v100 = capacity[SOC_TABLE_SIZE - 1].v100;

    // Constrain charge to the min and max v100 values
    charge = constrain(charge, min_v100, max_v100);

    // Interpolate the SoC value
    for (int i = 0; i < SOC_TABLE_SIZE - 1; i++) {
        if (capacity[i].v100 <= charge && capacity[i + 1].v100 >= charge) {
            float diffx = charge - capacity[i].v100;
            float diffn = capacity[i + 1].v100 - capacity[i].v100;

            return (int)(capacity[i].soc + (capacity[i + 1].soc - capacity[i].soc) * diffx / diffn);
        }
    }

    return 0; // Not in Range
}

float readADCValue(int pin) {
    return (float)analogRead(pin) + 0.5;
}

float calculateVoltage(int pin) {
    float adcValue = readADCValue(pin); 
    return (adcValue / 1024.0) * SCALE;
}

void setup() {
    Serial.begin(115200);
    while (!Serial);
}

void loop() {
    // Read the voltage from the battery
    float voltage = calculateVoltage(VBAT);

    // Convert voltage to hundredths of a volt to match the lookup table
    float charge = voltage * 100;

    // Calculate the state of charge (SoC) using the interpolate function
    uint16_t soc = interpolate(capacity, charge);

    // Print the voltage and state of charge to the Serial Monitor
    Serial.print("Voltage: ");
    Serial.print(voltage); // Print the actual voltage
    Serial.print(" V, SoC: ");
    Serial.print(soc);
    Serial.println(" %");

    // Wait for a second before the next reading
    delay(1000);
}
