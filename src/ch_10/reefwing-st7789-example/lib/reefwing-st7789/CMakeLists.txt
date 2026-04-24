# Copyright (c) 2026 David Such
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

add_library(reefwing-st7789
    reefwing_st7789.c
    st7789_lcd.pio
)

# Tell the SDK to generate st7789_lcd.pio.h
pico_generate_pio_header(reefwing-st7789 ${CMAKE_CURRENT_LIST_DIR}/st7789_lcd.pio)

target_include_directories(reefwing-st7789 PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(reefwing-st7789
    pico_stdlib
    hardware_pio
    hardware_interp
)