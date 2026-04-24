//--------------------------------------------------------------------+
// Reefwing ST7789 Example
//
// This example demonstrates how to use the Reefwing ST7789 driver
// with a Raspberry Pi Pico 2 to control an ST7789 display.
//
// Copyright (c) 2026 David Such
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT
//--------------------------------------------------------------------+

#include <stdio.h>
#include <stdlib.h> // for rand()

#include "pico/stdlib.h"
#include "reefwing_st7789.h"
#include "reefwing_rgb565_colors.h"

int main() {
    stdio_init_all();

    // Select your PIO and SM
    PIO pio = pio1;
    uint sm = 0;

    // Configure pin assignments and SPI options
    reefwing_st7789_config_t lcd_config = {
        .pin_bl = 17,
        .pin_dc = 18,
        .pin_rst = 19,
        .pin_cs = 20,
        .pin_din = 26,
        .pin_clk = 27,
        .spi_polarity = true,
        .clk_div = 2.0f
    };

    // Initialize the display
    reefwing_st7789_init(pio, sm, &lcd_config);

    // Fill the screen with a solid color
    reefwing_st7789_fill_screen(ST_RED);
    sleep_ms(2000);
    reefwing_st7789_fill_screen(ST_BLUE);
    sleep_ms(2000);

    // Draw 100 white pixels at random locations
    reefwing_st7789_fill_screen(ST_BLACK);
    for (int i = 0; i < 100; i++) {
        uint16_t rand_x = rand() % SCREEN_WIDTH;
        uint16_t rand_y = rand() % SCREEN_HEIGHT;

        reefwing_st7789_draw_pixel(rand_x, rand_y, ST_WHITE);
        sleep_ms(50);
    }
    sleep_ms(2000);

    reefwing_st7789_fill_screen(ST_BLACK);
    reefwing_st7789_draw_line(0, 0, 239, 319, ST_GOLD);      // diagonal
    reefwing_st7789_draw_line(10, 100, 230, 100, ST_ORANGE); // horizontal
    reefwing_st7789_draw_line(120, 10, 120, 300, ST_PINK);   // vertical
    sleep_ms(2000);

    reefwing_st7789_invert_display(true);  // Invert colors
    sleep_ms(1000);                        
    reefwing_st7789_invert_display(false); // Normal colors
    sleep_ms(1000);                       
    
    // Done — loop forever
    reefwing_st7789_fill_screen(ST_BLACK);
    while (true) {
        int rand_x = rand() % SCREEN_WIDTH;
        int rand_y = rand() % SCREEN_HEIGHT;
        uint16_t rand_color = rand() % 0xFFFF;

        reefwing_st7789_draw_pixel(rand_x, rand_y, rand_color);
    }
}
