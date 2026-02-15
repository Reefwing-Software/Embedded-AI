# Copyright (c) 2025 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# Microcontroller & Serial Port Configuration
MCU=atmega328p
F_CPU=16000000UL
PORT=$(shell ls /dev/cu.usbmodem* | head -n 1)  # Auto-detect Arduino port
BAUD=115200

# Toolchain Configuration
CC=avr-gcc
OBJCOPY=avr-objcopy
AVRDUDE=avrdude
CFLAGS=-mmcu=$(MCU) -Os -DF_CPU=$(F_CPU)

# Targets
all: blink.hex

blink.elf: blink.c
	$(CC) $(CFLAGS) -o blink.elf blink.c

blink.hex: blink.elf
	$(OBJCOPY) -O ihex blink.elf blink.hex

upload: blink.hex
	$(AVRDUDE) -c arduino -p $(MCU) -P $(PORT) -b $(BAUD) -U flash:w:blink.hex:i

clean:
	rm -f blink.elf blink.hex