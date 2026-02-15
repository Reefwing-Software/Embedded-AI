/**
 * Copyright (c) 2025 David Such
 * 
 * This software is released under the MIT License.
 * https://opensource.org/licenses/MIT
 */

#define F_CPU 16000000UL  // 16 MHz Clock
#include <avr/io.h>       // AVR Register Definitions

void timer1_delay_ms(uint16_t ms) {
    TCCR1B |= (1 << WGM12) | (1 << CS12) | (1 << CS10);  // CTC mode, Prescaler 1024
    OCR1A = (F_CPU / 1024 / 1000) * ms;  // Compare match value for the delay
    TCNT1 = 0;  // Reset Timer1 counter
    TIFR1 |= (1 << OCF1A);  // Clear previous interrupt flag
    while (!(TIFR1 & (1 << OCF1A)));  // Wait for timer to reach match value
}

int main(void) {
    DDRB |= (1 << DDB5);  // Set PB5 (pin 13) as output

    while (1) {
        PORTB ^= (1 << PORTB5);  // Toggle PB5 (LED ON/OFF)
        timer1_delay_ms(500);    // 500ms delay using Timer1
    }
}