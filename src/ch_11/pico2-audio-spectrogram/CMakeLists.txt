# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)

# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.1.1)
set(toolchainVersion 14_2_Rel1)
set(picotoolVersion 2.1.1)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================
set(PICO_BOARD pico2 CACHE STRING "Board type")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(pico2-audio-spectrogram C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add CMSIS headers globally before building DSP
include_directories(
    lib/CMSIS/CMSIS_6/CMSIS/Core/Include
    lib/CMSIS/headers
)

# Now add CMSIS-DSP
set(ARM_MATH_CM33 ON)  # tell CMSIS-DSP to build Cortex-M33
add_subdirectory(lib/CMSIS/CMSIS-DSP)

# Build the arm_cortexM33_math library manually
file(GLOB CMSIS_DSP_SRC
    lib/CMSIS/CMSIS-DSP/Source/BasicMathFunctions/*.c
    lib/CMSIS/CMSIS-DSP/Source/TransformFunctions/*.c
    lib/CMSIS/CMSIS-DSP/Source/CommonTables/*.c
    lib/CMSIS/CMSIS-DSP/Source/FastMathFunctions/*.c
    lib/CMSIS/CMSIS-DSP/Source/StatisticsFunctions/*.c
    lib/CMSIS/CMSIS-DSP/Source/MatrixFunctions/*.c
    lib/CMSIS/CMSIS-DSP/Source/ComplexMathFunctions/*.c
)

# Remove NEON-specific files that won't compile for M33
list(REMOVE_ITEM CMSIS_DSP_SRC
    ${CMAKE_CURRENT_SOURCE_DIR}/lib/CMSIS/CMSIS-DSP/Source/MatrixFunctions/_arm_mat_mult_neon.c
    ${CMAKE_CURRENT_SOURCE_DIR}/lib/CMSIS/CMSIS-DSP/Source/ComplexMathFunctions/_arm_cmplx_mult_neon.c
)

# Create the math library
add_library(arm_cortexM33_math ${CMSIS_DSP_SRC})

# Set include paths for CMSIS-DSP
target_include_directories(arm_cortexM33_math PUBLIC
    lib/CMSIS/CMSIS-DSP/Include
    lib/CMSIS/CMSIS_6/CMSIS/Core/Include
    lib/CMSIS/headers
)

# Compile definitions
target_compile_definitions(arm_cortexM33_math PUBLIC
    ARM_MATH_CM33
    ARM_MATH_LOOPUNROLL
)

# Add the display and microphone libraries
add_subdirectory(lib/reefwing-st7789)
add_subdirectory(lib/microphone-library-for-pico)

# Add RNNoise library
add_library(rnnoise STATIC
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/src/celt_lpc.c
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/src/denoise.c
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/src/kiss_fft.c
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/src/pitch.c
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/src/rnn.c
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/src/rnn_data.c
)

target_include_directories(rnnoise PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/include
    ${CMAKE_CURRENT_LIST_DIR}/lib/rnnoise/src
)

# Add executable. Default name is the project name, version 0.1
add_executable(pico2-audio-spectrogram 
    pico2-audio-spectrogram.c
    ${CMAKE_CURRENT_LIST_DIR}/lib/microphone-library-for-pico/examples/usb_microphone/usb_descriptors.c
    ${CMAKE_CURRENT_LIST_DIR}/lib/microphone-library-for-pico/examples/usb_microphone/usb_microphone.c
)

pico_set_program_name(pico2-audio-spectrogram "pico2-audio-spectrogram")
pico_set_program_version(pico2-audio-spectrogram "0.1")

# Modify the below lines to enable/disable output over UART/USB
pico_enable_stdio_uart(pico2-audio-spectrogram 0)
pico_enable_stdio_usb(pico2-audio-spectrogram 0)

# Add the standard include files to the build
target_include_directories(pico2-audio-spectrogram PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}
        lib/CMSIS/CMSIS-DSP/Include
        lib/microphone-library-for-pico/examples/usb_microphone
)

# Add the standard library to the build
target_link_libraries(pico2-audio-spectrogram
    hardware_pwm
    pico_stdlib
    arm_cortexM33_math
    pico_multicore
    tinyusb_device
    tinyusb_board
    pico_pdm_microphone
    rnnoise
    reefwing-st7789
    CMSISDSP
)

pico_add_extra_outputs(pico2-audio-spectrogram)
