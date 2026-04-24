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

 #include "reefwing_st7789.h"
 #include "hardware/gpio.h"
 #include "pico/stdlib.h"
 #include "st7789_lcd.pio.h"
 #include "font5x8.h"
 
 static const uint8_t st7789_init_seq[] = {
     1, 20, 0x01,                        // Software reset
     1, 10, 0x11,                        // Exit sleep mode
     2, 2, 0x3a, 0x55,                   // 16-bit color
     2, 0, 0x36, 0x00,                   // MADCTL
     5, 0, 0x2a, 0x00, 0x00, SCREEN_WIDTH >> 8, SCREEN_WIDTH & 0xff,   // CASET
     5, 0, 0x2b, 0x00, 0x00, SCREEN_HEIGHT >> 8, SCREEN_HEIGHT & 0xff, // RASET
     1, 2, 0x21,                         // Inversion on
     1, 2, 0x13,                         // Normal display on
     1, 2, 0x29,                         // Display on
     0                                   // End
 };
 
 // Store the current state machine and PIO so that reefwing_st7789_put() works
 static PIO current_pio;
 static uint current_sm;
 static reefwing_st7789_config_t current_config;
 
 static inline void lcd_set_dc_cs(bool dc, bool cs) {
     gpio_put_masked((1u << current_config.pin_dc) | (1u << current_config.pin_cs),
                     (!!dc << current_config.pin_dc) | (!!cs << current_config.pin_cs));
 }
 
 static void lcd_write_cmd(PIO pio, uint sm, const uint8_t *cmd, size_t count) {
     st7789_lcd_wait_idle(pio, sm);
     lcd_set_dc_cs(0, 0);
     st7789_lcd_put(pio, sm, *cmd++);
     if (count >= 2) {
         st7789_lcd_wait_idle(pio, sm);
         lcd_set_dc_cs(1, 0);
         for (size_t i = 0; i < count - 1; ++i)
             st7789_lcd_put(pio, sm, *cmd++);
     }
     st7789_lcd_wait_idle(pio, sm);
     lcd_set_dc_cs(1, 1);
 }
 
 static void lcd_init(PIO pio, uint sm, const uint8_t *init_seq) {
     const uint8_t *cmd = init_seq;
     while (*cmd) {
         lcd_write_cmd(pio, sm, cmd + 2, *cmd);
         sleep_ms(*(cmd + 1) * 5);
         cmd += *cmd + 2;
     }
 }
 
 void reefwing_st7789_init(PIO pio, uint sm, const reefwing_st7789_config_t *config) {
     // Store state for global access
     current_pio = pio;
     current_sm = sm;
     current_config = *config;
 
     uint offset = pio_add_program(pio, &st7789_lcd_program);
     st7789_lcd_program_init(pio, sm, offset, config->spi_polarity, config->pin_din,
                             config->pin_clk, config->clk_div);
 
     // Init pins
     gpio_init(config->pin_cs);
     gpio_init(config->pin_dc);
     gpio_init(config->pin_rst);
     gpio_init(config->pin_bl);
     gpio_set_dir(config->pin_cs, GPIO_OUT);
     gpio_set_dir(config->pin_dc, GPIO_OUT);
     gpio_set_dir(config->pin_rst, GPIO_OUT);
     gpio_set_dir(config->pin_bl, GPIO_OUT);
 
     // Display init sequence
     gpio_put(config->pin_cs, 1);
     gpio_put(config->pin_rst, 1);
     lcd_init(pio, sm, st7789_init_seq);
     gpio_put(config->pin_bl, 1);
 }
 
 void reefwing_st7789_start_pixels(void) {
     uint8_t cmd = 0x2c; // RAMWR

     lcd_write_cmd(current_pio, current_sm, &cmd, 1);
     lcd_set_dc_cs(1, 0);
 }
 
 void reefwing_st7789_put(uint16_t color) {
     st7789_lcd_put(current_pio, current_sm, color >> 8);
     st7789_lcd_put(current_pio, current_sm, color & 0xff);
 }

 void reefwing_st7789_set_window(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1) {
    uint8_t caset[] = {
        0x2A,
        x0 >> 8, x0 & 0xFF,
        x1 >> 8, x1 & 0xFF
    };
    uint8_t raset[] = {
        0x2B,
        y0 >> 8, y0 & 0xFF,
        y1 >> 8, y1 & 0xFF
    };

    lcd_write_cmd(current_pio, current_sm, caset, sizeof(caset));
    lcd_write_cmd(current_pio, current_sm, raset, sizeof(raset));
}
 
 void reefwing_st7789_set_cursor(uint16_t x, uint16_t y) {
    // Set a 1x1 pixel write window
    reefwing_st7789_set_window(x, y, x, y);
    reefwing_st7789_start_pixels(); // RAMWR + set to data mode
}

void reefwing_st7789_fill_screen(uint16_t color) {
    reefwing_st7789_set_window(0, 0, SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1);
    reefwing_st7789_start_pixels();

    for (int i = 0; i < SCREEN_WIDTH * SCREEN_HEIGHT; ++i) {
        reefwing_st7789_put(color);
    }
}

void reefwing_st7789_draw_line(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1, uint16_t color) {
    int dx = (x1 > x0) ? (x1 - x0) : (x0 - x1);
    int sx = (x0 < x1) ? 1 : -1;
    int dy = -((y1 > y0) ? (y1 - y0) : (y0 - y1));
    int sy = (y0 < y1) ? 1 : -1;
    int err = dx + dy; // error value e_xy

    while (true) {
        reefwing_st7789_set_cursor(x0, y0);
        reefwing_st7789_put(color);

        if (x0 == x1 && y0 == y1) break;

        int e2 = 2 * err;
        if (e2 >= dy) {
            err += dy;
            x0 += sx;
        }
        if (e2 <= dx) {
            err += dx;
            y0 += sy;
        }
    }
}

void reefwing_st7789_vertical_scroll(uint16_t row) {
    uint8_t data[] = {
        (row >> 8) & 0xFF,
        row & 0xFF
    };

    uint8_t cmd = 0x37; // Vertical Scroll Start Address
    lcd_write_cmd(current_pio, current_sm, &cmd, 1);
    lcd_set_dc_cs(1, 0); // Data mode
    st7789_lcd_put(current_pio, current_sm, data[0]);
    st7789_lcd_put(current_pio, current_sm, data[1]);
    //lcd_set_dc_cs(1, 1); // Deselect device
}

void reefwing_st7789_invert_display(bool invert) {
    uint8_t cmd = invert ? 0x20 : 0x21; // 0x21 = INVON, 0x20 = INVOFF
    lcd_write_cmd(current_pio, current_sm, &cmd, 1);
}

void reefwing_st7789_draw_pixel(uint16_t x, uint16_t y, uint16_t color) {
    reefwing_st7789_set_cursor(x, y);
    reefwing_st7789_put(color);
}
