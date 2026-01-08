class Battery {
public:
    static const int capacity = 1100;         // Battery capacity (mAh)
    static const int minChargeCurrent = 5;    // Minimum charge current (mA)
    static const int minVoltage = 3700;       // Minimum discharge voltage (mV)
    static const float senseResistor;         // Sense resistor (Ω)

    int cePin;
    int dacPin;

    // Measured values
    int current;
    int power;
    int soh;
    unsigned int voltage;
    unsigned int soc;
    unsigned int fullCapacity;
    unsigned int remainingCapacity;

    // Records charge cycles in the CYCLING state
    unsigned int chargeCycles; 
    bool cycling;

    // Constructor to initialize member variables
    Battery(int chargeEnablePin, int dacControlPin) 
        : current(0), power(0), soh(0), voltage(0), soc(0), 
          fullCapacity(0), remainingCapacity(0), chargeCycles(0), cycling(false), 
          cePin(chargeEnablePin), dacPin(dacControlPin) {}

    // Initialize hardware pins
    void begin() {
        pinMode(cePin, OUTPUT);
        pinMode(dacPin, OUTPUT);
        digitalWrite(cePin, HIGH);  // Turn charging off
        analogWriteResolution(8);   // DAC 8-bit resolution
        analogWrite(dacPin, 0);     // Turn DAC output off
    }

    void startCharging() const {
        digitalWrite(cePin, LOW);
    }

    void stopCharging() const {
        digitalWrite(cePin, HIGH);
    }

    void startDischarging(float dischargeRate) const {
        float targetVoltage = dischargeRate * senseResistor;  // Calculate the DAC voltage needed
        int dacValue = static_cast<int>(targetVoltage * 256.0 / 5.0);

        dacValue = constrain(dacValue, 0, 255);  // Ensure within DAC limits
        analogWrite(dacPin, dacValue);  // Set DAC output to initiate discharging
    }

    void stopDischarging() const {
        analogWrite(dacPin, 0);  // Set DAC output to 0 to stop discharging
    }

    bool charged() const {
        return current <= minChargeCurrent;
    }

    bool discharged() const {
        return voltage <= minVoltage;
    }
};

// Initialize static constant
const float Battery::senseResistor = 1.0;