/* Edge Impulse ingestion SDK
 * Copyright (c) 2022 EdgeImpulse Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
/* Includes --------------------------------------------------------------------- */
#include "ei_run_impulse.h"
#include "edge-impulse-sdk/porting/ei_classifier_porting.h"
#include "model-parameters/model_variables.h"
#include "ingestion-sdk-platform/sensors/ei_inertial.h"

bool _run_impulse = false;

/**
 * @brief      Start impulse, print settings
 */
void ei_run_nn_normal(void)
{
    _run_impulse = true;
    ei_start_stop_run_impulse(true);
    // summary of inferencing settings (from model_metadata.h)
    ei_printf("Inferencing settings:\n");
    ei_printf("\tInterval: ");
    ei_printf_float((float)EI_CLASSIFIER_INTERVAL_MS);
    ei_printf(" ms.\n");
    ei_printf("\tFrame size: %d\n", EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE);
    ei_printf("\tSample length: %d ms.\n", EI_CLASSIFIER_RAW_SAMPLE_COUNT / 16);
    ei_printf("\tNo. of classes: %d\n", sizeof(ei_classifier_inferencing_categories) /
            sizeof(ei_classifier_inferencing_categories[0]));

    ei_printf("Classes:\n");
    for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
        ei_printf("\t%s\n", ei_classifier_inferencing_categories[ix]);
    }

    ei_printf("Starting inferencing, press 'b' to break\n");
#ifdef WITH_IMU
    ei_inertial_prepare_impulse();
#endif
}

/**
 * @brief      Called from the ndp120 read out. Print classification output
 *             and send matched output string to user callback
 *
 * @param[in]  matched_feature
 */
void ei_classification_output(int matched_feature)
{
    if (_run_impulse == true) {

        ei_printf("\nMatch: %d\n", matched_feature);
        ei_printf("Predictions:\r\n");
        for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
            ei_printf("    %s: \t%d\r\n", ei_classifier_inferencing_categories[ix],
                (matched_feature == ix) ? 1 : 0);
        }

    }
}

/**
 * @brief 
 * 
 * @return true 
 * @return false 
 */
bool ei_run_impulse_is_active(void)
{
    return _run_impulse;
}

/**
 * @brief 
 * 
 */
void ei_run_impulse(void)
{
#ifdef WITH_IMU    
    ei_inertial_send_to_ndp(EI_CLASSIFIER_RAW_SAMPLES_PER_FRAME);
    ei_sleep(EI_CLASSIFIER_INTERVAL_MS);
    
#endif
}

/**
 * @brief 
 * 
 * @param start 
 */
void ei_start_stop_run_impulse(bool start)
{    
    _run_impulse = start;

    if(!start) {
        ei_printf("Inferencing stopped by user\r\n");
    }
}
