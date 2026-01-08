#define DAC         A0
#define V_PLUS      A1
#define V_MINUS     A2
#define OP_AMP_OUT  A3
#define I2C_SDA     A4
#define I2C_SCL     A5

#define UART_RX     RX
#define UART_TX     TX
#define TEMP_PIN    2     // DHT11 data pin
#define CE_PIN      3     // Charge Enable (Active Low)
#define GPOUT_PIN   4     // Battery gauge - battery low
#define MODE_BTN    5
#define START_BTN   6
#define LOG_SWITCH  7
#define CTRL_SWITCH 8
#define CD          9     // SD Card Detect
#define SPI_CS      10
#define SPI_MOSI    11
#define SPI_MISO    12
#define SPI_SCK     13

#define I2C_ADDR_OLED 0x3C

#define LOG_TEXT(logToCard) ((logToCard) ? "YES" : "NO")
#define CARD_TEXT(cardAvailable) ((cardAvailable) ? "SD Card OK" : "No SD Card")