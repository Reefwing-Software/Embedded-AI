//
// SPDX-FileCopyrightText: Copyright 2024 Arm Limited and/or its affiliates <open-source-office@arm.com>
// SPDX-License-Identifier: BSD-3-Clause
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pico/stdlib.h>

#include "rnnoise.h"

#define RNNOISE_VERSION_STRING "0.1.1"

//--------------------------------------------------------------------+
// MAIN
//--------------------------------------------------------------------+
// This example benchmarks the rnnoise_process_frame function from the RNNoise library.

int main()
{
  stdio_init_all();

  while (!stdio_usb_connected()) {
    tight_loop_contents();
  }

  printf("RNNoise Benchmark\n");
  printf("RNNoise version: %s\n", RNNOISE_VERSION_STRING);

  DenoiseState* st = rnnoise_create(NULL);

  #define FRAME_SIZE 480
  float x[FRAME_SIZE];

  // run once without timing to init
  memset(x, 0x00, sizeof(x));
  rnnoise_process_frame(st, x, x);

  const int benchmark_iterations = 100;
  absolute_time_t rnnoise_process_frame_time = 0;

  for (int j = 0; j < benchmark_iterations; j++) {
    for (int i = 0; i < FRAME_SIZE; i++) {
      x[i] = ((float)rand()) / ((float)RAND_MAX) * 0x7fff;
    }

    absolute_time_t usec_rnnoise_process_frame_start = get_absolute_time();

    rnnoise_process_frame(st, x, x);

    absolute_time_t usec_rnnoise_process_frame_end = get_absolute_time();

    rnnoise_process_frame_time += (usec_rnnoise_process_frame_end - usec_rnnoise_process_frame_start);
  }

  printf("rnnoise_process_frame %llu usec\n", (rnnoise_process_frame_time / benchmark_iterations));

  while (1) {
    tight_loop_contents();
  }

  return 0;
}
