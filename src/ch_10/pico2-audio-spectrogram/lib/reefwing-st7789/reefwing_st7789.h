//--------------------------------------------------------------------+
// Reefwing ST7789 LCD Driver for the DFR0664 Display and Pico 2.
//
// This driver is based on the ST7789 LCD code from the Pico examples
// https://github.com/raspberrypi/pico-examples/tree/master/pio/st7789_lcd
// 
// The original code is released under the SPDX-License-Identifier: BSD-3-Clause
// Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
//
// This modified version makes the SPI clock polarity configurable
// and provides a simple API for drawing images.
// Copyright (c) 2025 David Such
//--------------------------------------------------------------------+

#ifndef REEFWING_ST7789_H
#define REEFWING_ST7789_H

#include "hardware/pio.h"

#define SCREEN_WIDTH  240
#define SCREEN_HEIGHT 320

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    uint pin_bl;       // Backlight
    uint pin_dc;       // Data/Command
    uint pin_rst;      // Reset
    uint pin_cs;       // Chip Select
    uint pin_din;      // Data In (MOSI)
    uint pin_clk;      // Clock (SCLK)
    bool spi_polarity; // SPI Clock Polarity
    float clk_div;     // Serial clock divider
} reefwing_st7789_config_t;

/**
 * @brief Initialize the ST7789 display with a custom configuration.
 *
 * @param pio The PIO instance (pio0 or pio1).
 * @param sm The state machine number (0-3).
 * @param config Pointer to the configuration structure.
 */
void reefwing_st7789_init(PIO pio, uint sm, const reefwing_st7789_config_t *config);

/**
 * @brief Issue the RAMWR command and prepare for pixel transmission.
 */
void reefwing_st7789_start_pixels(void);

/**
 * @brief Send a 16-bit RGB565 pixel to the display.
 *
 * @param color The color to send (RGB565 format).
 */
void reefwing_st7789_put(uint16_t color);

/**
 * @brief Move the ST7789 write cursor to (x, y).
 *
 * @param x   X-coordinate (column).
 * @param y   Y-coordinate (row).
 */
void reefwing_st7789_set_cursor(uint16_t x, uint16_t y);

/**
 * @brief Set a drawing window from (x0, y0) to (x1, y1)
 */
void reefwing_st7789_set_window(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1);

/**
 * @brief Fill the entire screen with a solid RGB565 color.
 *
 * @param color The RGB565 color value.
 */
void reefwing_st7789_fill_screen(uint16_t color);

/**
 * @brief Draw a straight line between two points using Bresenham's algorithm.
 *
 * @param x0 Starting x-coordinate.
 * @param y0 Starting y-coordinate.
 * @param x1 Ending x-coordinate.
 * @param y1 Ending y-coordinate.
 * @param color RGB565 color to draw the line.
 */
void reefwing_st7789_draw_line(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1, uint16_t color);

/**
 * @brief Set the vertical scroll start address (row 0 to SCREEN_HEIGHT - 1)
 *
 * @param row  The starting row for vertical scrolling.
 */
void reefwing_st7789_vertical_scroll(uint16_t row);

/**  
 * @brief Set the display to normal mode or inverted mode.
 *
 * @param invert true for inverted mode, false for normal mode.
 */
void reefwing_st7789_invert_display(bool invert);

/**
 * @brief  Draw a single pixel at (x, y) with the specified color.
 * 
 * @param x x-coordinate (column).
 * @param y y-coordinate (row).
 * @param color RGB565 color to draw the pixel.
 */
void reefwing_st7789_draw_pixel(uint16_t x, uint16_t y, uint16_t color);

#ifdef __cplusplus
}
#endif

#endif // REEFWING_ST7789_H