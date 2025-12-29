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
/* Include ----------------------------------------------------------------- */
#include "ei_microphone.h"
#include "ei_syntiant_ndp120.h"

#include "mbed.h"
#include "rtos.h"
#include "Thread.h"
#include "firmware-sdk/sensor_aq.h"
#include "edge-impulse-sdk/porting/ei_classifier_porting.h"
#include "ingestion-sdk-platform/nicla_syntiant/ei_device_syntiant_nicla.h"
#include "sensor_aq_mbedtls/sensor_aq_mbedtls_hs256.h"
#include "firmware-sdk/sensor_aq.h"
#include "NDP.h"

/* Constant ---------------------------------------------------------------- */

/* Types ***---------------------------------------------------------------- */

/** Status and control struct for inferencing struct */
typedef struct {
    int16_t     *buffers[2];
    uint8_t     buf_select;
    uint8_t     buf_ready;
    uint32_t    buf_count;
    uint32_t    n_samples;
} inference_t;

/* Private functions ------------------------------------------------ */
static size_t ei_write(const void *buffer, size_t size, size_t count, EI_SENSOR_AQ_STREAM * stream);
static int ei_seek(EI_SENSOR_AQ_STREAM * stream, long int offset, int origin);
static int insert_ref(char *buffer, int hdrLength);
static bool create_header(sensor_aq_payload_info *payload);

#ifndef WITH_IMU
static void mic_thread_function(void);

/* Private variables ------------------------------------------------------- */

static uint8_t local_mic_stack[10 * 1024];
#endif
//static rtos::Thread mic_thread(osPriorityNormal7, sizeof(local_mic_stack), local_mic_stack, "mic-thread");
static inference_t inference;
static uint32_t required_samples_size;
static uint32_t headerOffset = 0;
microphone_sample_t *sample_buffer_processed;

static uint32_t current_sample;
static bool sampling_finished;
static uint32_t required_samples;

/* hash stuff */
static unsigned char ei_mic_ctx_buffer[1024];
static sensor_aq_signing_ctx_t ei_mic_signing_ctx;
static sensor_aq_mbedtls_hs256_ctx_t ei_mic_hs_ctx;
static sensor_aq_ctx ei_mic_ctx = {
    { ei_mic_ctx_buffer, 1024 },
    &ei_mic_signing_ctx,
    &ei_write,
    &ei_seek,
    NULL,
};

/**
 * @brief 
 * 
 */
void ei_microphone_start_stream(void)
{
    //mic_thread.start(mbed::callback(mic_thread_function));    
}

/**
 * @brief Initialize the ingestion 
 * 
 * @return true 
 * @return false 
 */
bool ei_microphone_start_sampling(void)
{
#ifndef WITH_IMU
    rtos::Thread* mic_thread;
    EiDeviceSyntiantNicla *dev = static_cast<EiDeviceSyntiantNicla*>(EiDeviceInfo::get_device());
    EiExtFlashMemory* ext_mem = dev->get_ext_flash();
    uint8_t *page_buffer;
    int ret;    

    sensor_aq_payload_info payload = {
        dev->get_device_id().c_str(),
        dev->get_device_type().c_str(),
        dev->get_sample_interval_ms(),
        { { "audio", "wav" } }
    };

    ei_printf("Sampling settings:\n");
    ei_printf("\tInterval: %.5f ms.\n", dev->get_sample_interval_ms());
    ei_printf("\tLength: %lu ms.\n", dev->get_sample_length_ms());
    ei_printf("\tName: %s\n", dev->get_sample_label().c_str());
    ei_printf("\tHMAC Key: %s\n", dev->get_sample_hmac_key().c_str());
    ei_printf("\tFile name: %s\n", dev->get_sample_label().c_str());

    required_samples = (uint32_t)((dev->get_sample_length_ms()) / dev->get_sample_interval_ms());

    /* Round to even number of samples for word align flash write */
    if(required_samples & 1) {
        required_samples++;
    }

    required_samples_size = required_samples * sizeof(microphone_sample_t);
    current_sample = 0;

    /*
     * TODO check if enough space
     */
    ei_printf("Starting in 2000 ms... (or until all flash was erased)\n");
    uint32_t start_time = rtos::Kernel::get_ms_count();
    ret = ext_mem->erase_sample_data(0, required_samples_size);
    uint32_t stop_time = rtos::Kernel::get_ms_count();

    if ((stop_time - start_time) < 2000){
        ei_sleep(2000 - (stop_time - start_time));
    }    

    if (create_header(&payload) == false) {
        return false;
    }
    
    mic_thread = new rtos::Thread(osPriorityNormal7, sizeof(local_mic_stack), local_mic_stack, "mic-thread");
    
    sampling_finished = false;
    mic_thread->start(mbed::callback(mic_thread_function));
    
    while(!sampling_finished){
        rtos::ThisThread::sleep_for(100);
    }

    mic_thread->terminate();    // needed ?
    mic_thread->join();
#if 1

    uint8_t final_byte[] = {0xff};
    int ctx_err = ei_mic_ctx.signature_ctx->update(ei_mic_ctx.signature_ctx, final_byte, 1);
    if (ctx_err != 0) {
        return ctx_err;
    }

    // finish the signing
    ctx_err =
        ei_mic_ctx.signature_ctx->finish(ei_mic_ctx.signature_ctx, ei_mic_ctx.hash_buffer.buffer);
#else
    ret = ei_mic_ctx.signature_ctx->finish(ei_mic_ctx.signature_ctx, ei_mic_ctx.hash_buffer.buffer);
    if (ret != 0) {
        ei_printf("Failed to finish signature (%d)\n", ret);
        return false;
    }
#endif

    ei_printf("Done sampling, total bytes collected: %lu\n", required_samples_size);
    ei_printf("[1/1] Uploading file to Edge Impulse...\n");
    ei_printf("Not uploading file, not connected to WiFi. Used buffer, from=0, to=%lu.\n", required_samples_size + headerOffset);
    ei_printf("OK\n");

    return true;
#else
    return false;
#endif
}

/**
 * @brief 
 * 
 */
void ei_microphone_stop_stream(void)
{
    //mic_thread.terminate();
    //mic_thread.join();
}

#ifndef WITH_IMU
/**
 * @brief 
 * 
 */
static void mic_thread_function(void)
{
    EiDeviceSyntiantNicla *dev = static_cast<EiDeviceSyntiantNicla*>(EiDeviceInfo::get_device());
    EiExtFlashMemory* ext_mem = dev->get_ext_flash();
    const uint16_t read_size = (768); // Every time I try to read 24 * x ms
    const uint16_t _samples = read_size*3;
    uint16_t read = 0;
    uint8_t _local_audio_buffer[_samples] = {0};
    uint32_t _local_current_samples = 0;
    unsigned int len = 0;    
    int s = 0;

    ei_printf("Mic thread: required samples %d\n", required_samples);

    ei_syntiant_clear_match();
    NDP.noInterrupts();

    do {
        s = NDP.extractData(_local_audio_buffer, &len); /* we want to unload the previous buffer */
    }while(s != 0);
    ei_printf("Latest retval: %d\n", s);

    ei_printf("Sampling...\n");
    nicla::leds.setColor(green);

    while(_local_current_samples < required_samples) {
        
        //start_time = rtos::Kernel::get_ms_count();
        s = NDP.extractData(&_local_audio_buffer[read], &len);
        //stop_time = rtos::Kernel::get_ms_count();
        //ei_printf("Reading %u samples took %d with retval %d\n", len, (stop_time - start_time), s);

        if (len !=0) {
            read += len;
            if (read >= read_size*2) {
                ext_mem->write_sample_data(_local_audio_buffer, headerOffset + (_local_current_samples * 2), read);
                _local_current_samples += (read/2);
                read = 0;
            }

            //ei_sleep(1);    // give a little time ?
        }
        else{
            ei_printf("len 0 with retvalue: %ld\n", s);
            ei_sleep(1);    // give a little time ?
        }
        
    }

    ei_syntiant_set_match();
    NDP.interrupts();
    nicla::leds.setColor(off);

    sampling_finished = true;
}
#endif
/**
 * @brief Create a header object
 * 
 * @param payload 
 * @return true 
 * @return false 
 */
static bool create_header(sensor_aq_payload_info *payload)
{
    int ret;
    EiDeviceSyntiantNicla *dev = static_cast<EiDeviceSyntiantNicla*>(EiDeviceInfo::get_device());
    EiExtFlashMemory* ext_mem = dev->get_ext_flash();

    sensor_aq_init_mbedtls_hs256_context(&ei_mic_signing_ctx, &ei_mic_hs_ctx, dev->get_sample_hmac_key().c_str());

    ret = sensor_aq_init(&ei_mic_ctx, payload, NULL, true);

    if (ret != AQ_OK) {
        ei_printf("sensor_aq_init failed (%d)\n", ret);
        return false;
    }

    // then we're gonna find the last byte that is not 0x00 in the CBOR buffer.
    // That should give us the whole header
    size_t end_of_header_ix = 0;
    for (size_t ix = ei_mic_ctx.cbor_buffer.len - 1; ix != 0; ix--) {
        if (((uint8_t *)ei_mic_ctx.cbor_buffer.ptr)[ix] != 0x0) {
            end_of_header_ix = ix;
            break;
        }
    }

    if (end_of_header_ix == 0) {
        ei_printf("Failed to find end of header\n");
        return false;
    }

    int ref_size = insert_ref(((char*)ei_mic_ctx.cbor_buffer.ptr + end_of_header_ix), end_of_header_ix);
    // and update the signature
    ret = ei_mic_ctx.signature_ctx->update(ei_mic_ctx.signature_ctx, (uint8_t*)(ei_mic_ctx.cbor_buffer.ptr + end_of_header_ix), ref_size);
    if (ret != 0) {
        ei_printf("Failed to update signature from header (%d)\n", ret);
        return false;
    }
    end_of_header_ix += ref_size;

    // Write to blockdevice
    ei_printf("Trying to write %ld byte", end_of_header_ix);
    ret = ext_mem->write_sample_data((uint8_t*)ei_mic_ctx.cbor_buffer.ptr, 0, end_of_header_ix);
    if ((size_t)ret != end_of_header_ix) {
        ei_printf("Failed to write to header blockdevice (%d)\n", ret);
        return false;
    }

    headerOffset = end_of_header_ix;

    return true;
}

/**
 *
 * @param buffer
 * @param hdrLength
 * @return
 */
static int insert_ref(char *buffer, int hdrLength)
{
    #define EXTRA_BYTES(a)  ((a & 0x3) ? 4 - (a & 0x3) : (a & 0x03))
    const char *ref = "Ref-BINARY-i16";
    int addLength = 0;
    int padding = EXTRA_BYTES(hdrLength);

    buffer[addLength++] = 0x60 + 14 + padding;
    for(unsigned int i = 0; i < strlen(ref); i++) {
        buffer[addLength++] = *(ref + i);
    }
    for(int i = 0; i < padding; i++) {
        buffer[addLength++] = ' ';
    }

    buffer[addLength++] = 0xFF;

    return addLength;
}

/* Dummy functions for sensor_aq_ctx type */
/**
 *
 * @param
 * @param size
 * @param count
 * @param
 * @return
 */
static size_t ei_write(const void* buffer, size_t size, size_t count, EI_SENSOR_AQ_STREAM* stream)
{
    (void)buffer;
    (void)size;
    (void)stream;

    return count;
}

/**
 *
 * @param
 * @param offset
 * @param origin
 * @return
 */
static int ei_seek(EI_SENSOR_AQ_STREAM* stream, long int offset, int origin)
{
    (void)stream;
    (void)offset;
    (void)origin;

    return 0;
}
