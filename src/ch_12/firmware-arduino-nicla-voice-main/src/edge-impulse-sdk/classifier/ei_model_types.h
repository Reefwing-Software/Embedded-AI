/*
 * Copyright (c) 2022 EdgeImpulse Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an "AS
 * IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language
 * governing permissions and limitations under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef _EDGE_IMPULSE_MODEL_TYPES_H_
#define _EDGE_IMPULSE_MODEL_TYPES_H_

#include <stdint.h>

#include "edge-impulse-sdk/classifier/ei_classifier_types.h"

#define EI_CLASSIFIER_NONE                       255
#define EI_CLASSIFIER_UTENSOR                    1
#define EI_CLASSIFIER_TFLITE                     2
#define EI_CLASSIFIER_CUBEAI                     3
#define EI_CLASSIFIER_TFLITE_FULL                4
#define EI_CLASSIFIER_TENSAIFLOW                 5
#define EI_CLASSIFIER_TENSORRT                   6
#define EI_CLASSIFIER_DRPAI                      7
#define EI_CLASSIFIER_TFLITE_TIDL                8
#define EI_CLASSIFIER_AKIDA                      9
#define EI_CLASSIFIER_SYNTIANT                   10
#define EI_CLASSIFIER_ONNX_TIDL                  11

#define EI_CLASSIFIER_SENSOR_UNKNOWN             -1
#define EI_CLASSIFIER_SENSOR_MICROPHONE          1
#define EI_CLASSIFIER_SENSOR_ACCELEROMETER       2
#define EI_CLASSIFIER_SENSOR_CAMERA              3
#define EI_CLASSIFIER_SENSOR_9DOF                4
#define EI_CLASSIFIER_SENSOR_ENVIRONMENTAL       5
#define EI_CLASSIFIER_SENSOR_FUSION              6

// These must match the enum values in TensorFlow Lite's "TfLiteType"
#define EI_CLASSIFIER_DATATYPE_FLOAT32           1
#define EI_CLASSIFIER_DATATYPE_INT8              9

#define EI_CLASSIFIER_LAST_LAYER_UNKNOWN               -1
#define EI_CLASSIFIER_LAST_LAYER_SSD                   1
#define EI_CLASSIFIER_LAST_LAYER_FOMO                  2
#define EI_CLASSIFIER_LAST_LAYER_YOLOV5                3
#define EI_CLASSIFIER_LAST_LAYER_YOLOX                 4
#define EI_CLASSIFIER_LAST_LAYER_YOLOV5_V5_DRPAI       5
#define EI_CLASSIFIER_LAST_LAYER_YOLOV7                6

struct ei_impulse;

typedef struct {
    uint16_t implementation_version;
    bool is_configured;
    uint32_t average_window_duration_ms;
    float detection_threshold;
    uint32_t suppression_ms;
    uint32_t suppression_flags;
} ei_performance_calibration_config_t;

#endif // _EDGE_IMPULSE_MODEL_TYPES_H_
