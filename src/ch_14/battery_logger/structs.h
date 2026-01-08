struct SampleRate {
    int intervalSeconds;  // Interval in seconds
    const char* name;     // Descriptive name
};

struct DischargeMode {
    const char* name;
    float rate;      // Discharge rate in A
    char shortName;  // Short identifier, e.g., 'S', 'M', 'F'
};