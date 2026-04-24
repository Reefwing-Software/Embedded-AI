//--------------------------------------------------------------------+
// Copyright (c) 2026 David Such
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT
//
// This file defines color constants for the ST7789 display.
// The colors are defined in RGB565 format, which is a 16-bit color representation.
// RGB565 format uses 5 bits for red, 6 bits for green, and 5 bits for blue.
//--------------------------------------------------------------------+

#ifndef REEFWING_ST7789_COLORS_H
#define REEFWING_ST7789_COLORS_H

// Macros to convert RGB888 to RGB565
// RGB888 format uses 8 bits for each color channel (red, green, blue).
#define RGB565(r, g, b) (((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3))

// Primary Colors
#define ST_BLACK   0x0000
#define ST_WHITE   0xFFFF
#define ST_RED     0xF800
#define ST_GREEN   0x07E0
#define ST_BLUE    0x001F

// Secondary Colors
#define ST_CYAN    0x07FF
#define ST_MAGENTA 0xF81F
#define ST_YELLOW  0xFFE0

// Grayscale Variants
#define ST_LIGHTGRAY   0xC618
#define ST_GRAY        0x8410
#define ST_DARKGRAY    0x4208

// Extra Colors
#define ST_ORANGE      0xFD20
#define ST_PINK        0xFC9F
#define ST_PURPLE      0x8010
#define ST_BROWN       0xA145
#define ST_GOLD        0xFEA0
#define ST_SILVER      0xC618
#define ST_SKYBLUE     0x867D
#define ST_NAVY        0x000F
#define ST_TEAL        0x0438
#define ST_MAROON      0x8000
#define ST_OLIVE       0x8400
#define ST_FOREST      0x03E0

#endif // REEFWING_ST7789_COLORS_H