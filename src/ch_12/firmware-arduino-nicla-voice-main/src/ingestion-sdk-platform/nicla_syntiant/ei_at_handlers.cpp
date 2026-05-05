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
#include "ei_at_handlers.h"
#include "Serial.h"
#include "drivers/UnbufferedSerial.h"
#include "edge-impulse-sdk/porting/ei_classifier_porting.h"
#include "ei_syntiant_ndp120.h"
#include "ei_fusion.h"
#include "inference/ei_run_impulse.h"

#include "mbed.h"
#include "rtos.h"
#include "Thread.h"
#include "EventQueue.h"

#include "at_base64_lib.h"

#define AT_LISTFILE                 "LISTFILES"
#define AT_LISTFILE_HELP_TEXT       "Lists file"
#define AT_UPDATEFILE               "UPDATEFILE"
#define AT_UPDATEFILE_HELP_TEXT     "Update model"
#define AT_UPDATEFILE_ARGS          "FILENAME"
#define AT_FORMATEXTFLASH           "FORMATEXTFLASH"
#define AT_FORMATEXTFLASH_HELP_TEXT "Format the external flash"

typedef struct{
    char rx_buffer[512];
    uint16_t index;
}serial_buffer_t;

//static ATServer *pat = nullptr;
EiDeviceSyntiantNicla *pei_device;

static bool at_list_config(void);
static bool at_clear_config(void);
static bool at_device_info(void);
static bool at_get_sample_settings(void);
static bool at_set_sample_settings(const char **argv, const int argc);
static bool at_get_upload_settings(void);
static bool at_set_upload_settings(const char **argv, const int argc);
static bool at_set_upload_host(const char **argv, const int argc);
static bool at_list_sensors(void);
static bool at_list_fusion_sensors(void);
static bool at_sample_start(const char **argv, const int argc);
static bool at_run_nn_normal(void);
static bool at_run_nn_normal_cont(void);
static bool at_get_mgmt_settings(void);
static bool at_set_mgmt_settings(const char **argv, const int argc);
static bool at_unlink_file(const char **argv, const int argc);
static bool at_read_buffer(const char **argv, const int argc);
static bool at_read_raw(const char **argv, const int argc);
static bool at_read_encode_send_sample_buffer(size_t start, size_t length);
static inline bool check_args_num(const int &required, const int &received);

static bool at_list_file(void);
static bool at_update_file(const char **argv, const int argc);
static bool at_format_ext_flash(void);

/* Public functions -------------------------------------------------------- */
/**
 *
 * @return
 */
ATServer * ei_at_init(EiDeviceSyntiantNicla *ei_device)
{   
    ATServer *pat;
    pat = ATServer::get_instance();
    pei_device = ei_device;

    pat->register_command(AT_CONFIG, AT_CONFIG_HELP_TEXT, nullptr, at_list_config, nullptr, nullptr);
    pat->register_command(AT_CLEARCONFIG, AT_CLEARCONFIG_HELP_TEXT, at_clear_config, nullptr, nullptr, nullptr);
    pat->register_command(AT_SAMPLESTART, AT_SAMPLESTART_HELP_TEXT, nullptr, nullptr, at_sample_start, AT_SAMPLESTART_ARGS);
    pat->register_command(AT_SAMPLESETTINGS, AT_SAMPLESETTINGS_HELP_TEXT, nullptr, at_get_sample_settings, at_set_sample_settings, AT_SAMPLESETTINGS_ARGS);
    pat->register_command(AT_RUNIMPULSE, AT_RUNIMPULSE_HELP_TEXT, at_run_nn_normal, nullptr, nullptr, nullptr);
    pat->register_command(AT_RUNIMPULSECONT, AT_RUNIMPULSECONT_HELP_TEXT, at_run_nn_normal_cont, nullptr, nullptr, nullptr);
    pat->register_command(AT_READBUFFER, AT_READBUFFER_HELP_TEXT, nullptr, nullptr, at_read_buffer, AT_READBUFFER_ARGS);
    pat->register_command(AT_MGMTSETTINGS, AT_MGMTSETTINGS_HELP_TEXT, nullptr, at_get_mgmt_settings, at_set_mgmt_settings, AT_MGMTSETTINGS_ARGS);
    pat->register_command(AT_UPLOADSETTINGS, AT_UPLOADSETTINGS_HELP_TEXT, nullptr, at_get_upload_settings, at_set_upload_settings, AT_UPLOADSETTINGS_ARGS);
    pat->register_command(AT_UPLOADHOST, AT_UPLOADHOST_HELP_TEXT, nullptr, nullptr, at_set_upload_host, AT_UPLOADHOST_ARGS);
    pat->register_command(AT_READRAW, AT_READRAW_HELP_TEXT, nullptr, nullptr, at_read_raw, AT_READRAW_ARS);
    pat->register_command(AT_UNLINKFILE, AT_UNLINKFILE_HELP_TEXT, nullptr, nullptr, at_unlink_file, AT_UNLINKFILE_ARGS);

    pat->register_command(AT_LISTFILE, AT_LISTFILE_HELP_TEXT, nullptr, at_list_file, nullptr, nullptr);
    pat->register_command(AT_UPDATEFILE, AT_UPDATEFILE_HELP_TEXT, nullptr, nullptr, at_update_file, AT_UPDATEFILE_ARGS);

    pat->register_command(AT_FORMATEXTFLASH, AT_FORMATEXTFLASH_HELP_TEXT, at_format_ext_flash, nullptr, nullptr, nullptr);
    

    #if 0
    _mbed_serial* pserial;    
    if (Serial)
    {
        mbed::FileHandle *fp = &(*Serial);
        //mbed::UnbufferedSerial *unser = static_cast<mbed::UnbufferedSerial*>(fp);
        //unser->attach(mbed::Callback<void()>(&at_rx_irq));
        //suggestion from Martino
        mbed::UnbufferedSerial* unser = (mbed::UnbufferedSerial*)static_cast<mbed::FileHandle*>(Serial);
        unser->attach(mbed::callback(&at_rx_irq), mbed::SerialBase::RxIrq);
    }    
    #endif
    
    //at_server_thread.start(mbed::callback(at_server_function));

    //queue.call_every(10, mbed::callback(&at_rx_irq));
    //queue.dispatch_forever();

    return pat;
}

/* Private functions ------------------------------------------------------- */

/**
 * @brief 
 * 
 * @return true 
 * @return false 
 */
bool at_list_config(void)
{    
    ei_printf("===== Device info =====\n");
    at_device_info();
    ei_printf("\n");
    ei_printf("===== Sensors ======\n");
    at_list_sensors();
    at_list_fusion_sensors();
    ei_printf("\n");
    ei_printf("===== Snapshot ======\n");
    ei_printf("Has snapshot:    0\n");
    ei_printf("\n");
    ei_printf("===== WIFI =====\n");
    ei_printf("SSID:      \n");
    ei_printf("Password:  \n");
    ei_printf("Security:  0\n");
    ei_printf("MAC:       00:00:00:00:00:00\n");
    ei_printf("Connected: 0\n");
    ei_printf("Present:   0\n");
    ei_printf("\n");
    ei_printf("===== Sampling parameters =====\n");
    at_get_sample_settings();
    ei_printf("\n");
    ei_printf("===== Upload settings =====\n");
    at_get_upload_settings();
    ei_printf("\n");
    ei_printf("===== Remote management =====\n");
    at_get_mgmt_settings();
    ei_printf("\n");
    
    return true;
}

/**
 * @brief 
 * 
 * @return 
 */
static bool at_clear_config(void)
{
    bool ret_val = false;

    if (pei_device != nullptr)
    {
        ei_printf("Clearing config and restarting system...\n");
        pei_device->clear_config();
        ret_val = true;
    }
    else
    {

    }
    
    return ret_val;
}

/**
 * @brief brief description
 * 
 * @return
 */
static bool at_device_info(void)
{
    bool ret_val = false;
    ei_syntiant_clear_match();
    if (pei_device != nullptr)
    {
        ei_printf("ID:         %s\n", pei_device->get_device_id().c_str());
        ei_printf("Type:       %s\n", pei_device->get_device_type().c_str());
        ei_printf("AT Version: %s\n", AT_COMMAND_VERSION);
        ei_printf("Data Transfer Baudrate: %lu\n", pei_device->get_max_data_output_baudrate());
        ret_val = true;
    }
    else
    {

    }
    ei_syntiant_set_match();

    return ret_val;
}

/**
 * @brief 
 * 
 * @return true 
 * @return false 
 */
static bool at_get_sample_settings(void)
{
    bool ret_val = false;

    if (pei_device != nullptr)
    {
        ei_printf("Label:     %s\n", pei_device->get_sample_label().c_str());
        ei_printf("Interval:  ");
        ei_printf_float(pei_device->get_sample_interval_ms());
        ei_printf(" ms.\n");
        ei_printf("Length:    %lu ms.\n", pei_device->get_sample_length_ms());
        ei_printf("HMAC key:  %s\n", pei_device->get_sample_hmac_key().c_str());
        ret_val = true;
    }
    else
    {

    }
    ei_syntiant_set_match();
    
    return ret_val;
}

/**
 * @brief 
 * 
 * @param argv 
 * @param argc 
 * @return true 
 * @return false 
 */
static bool at_set_sample_settings(const char **argv, const int argc)
{
    if ((argc < 3) || (pei_device == nullptr)) {
        ei_printf("Missing argument! Required: " AT_SAMPLESETTINGS_ARGS "\n");
        return false;
    }

    pei_device->set_sample_label(argv[0]);

    //TODO: sanity check and/or exception handling
    std::string interval_ms_str(argv[1]);
    pei_device->set_sample_interval_ms(stof(interval_ms_str));

    //TODO: sanity check and/or exception handling
    std::string sample_length_str(argv[2]);
    pei_device->set_sample_length_ms(stoi(sample_length_str));

    if(argc >= 4) {
        pei_device->set_sample_hmac_key(argv[3]);
    }

    ei_printf("OK\n");

    return true;
}

/**
 * @brief 
 * 
 * @return true 
 * @return false 
 */
static bool at_get_upload_settings(void)
{
    bool ret_val = false;

    if (pei_device != nullptr)
    {
        ei_printf("Api Key:   %s\n", pei_device->get_upload_api_key().c_str());
        ei_printf("Host:      %s\n", pei_device->get_upload_host().c_str());
        ei_printf("Path:      %s\n", pei_device->get_upload_path().c_str());

        ret_val = true;
    }
    else
    {

    }
    ei_syntiant_set_match();

    return ret_val;
}

/**
 * @brief 
 * 
 * @param argv 
 * @param argc 
 * @return true 
 * @return false 
 */
static bool at_set_upload_settings(const char **argv, const int argc)
{
    bool ret_val = false;

    if (check_args_num(2, argc) == false) {
        return false;
    }
    if (pei_device != nullptr)
    {
        pei_device->set_upload_api_key(argv[0]);
        pei_device->set_upload_host(argv[1]);

        ret_val = true;
    }

    ei_printf("OK\n");

    return ret_val;
}

/**
 * @brief 
 * 
 * @param argv 
 * @param argc 
 * @return true 
 * @return false 
 */
static bool at_set_upload_host(const char **argv, const int argc)
{
    bool ret_val = false;

    if (check_args_num(1, argc) == false) {
        return false;
    }

    if (pei_device != nullptr)
    {
        pei_device->set_upload_host(argv[0]);
        ret_val = true;
    }

    ei_printf("OK\n");

    return ret_val;
}

/**
 * @brief 
 * 
 * @return true 
 * @return false 
 */
static bool at_list_sensors(void)
{
    bool ret_val = false;
    const ei_device_sensor_t *list;
    size_t list_size;

    if (pei_device != nullptr)
    {
        bool r = pei_device->get_sensor_list((const ei_device_sensor_t **)&list, &list_size);
        if (r != true) {
            ei_printf("Failed to get sensor list (%d)\n", r);
            return true;
        }
        ret_val = true;

        for (size_t ix = 0; ix < list_size; ix++) {
            ei_printf(
                "Name: %s, Max sample length: %hus, Frequencies: [",
                list[ix].name,
                list[ix].max_sample_length_s);
            for (size_t fx = 0; fx < EI_MAX_FREQUENCIES; fx++) {
                if (list[ix].frequencies[fx] != 0.0f) {
                    if (fx != 0) {
                        ei_printf(", ");
                    }
                    ei_printf_float(list[ix].frequencies[fx]);
                    ei_printf("Hz");
                }
            }
            ei_printf("]\n");
        }
    }
    else
    {

    }
    ei_syntiant_set_match();

    return ret_val;
}

/**
 * @brief 
 * 
 * @return true 
 * @return false 
 */
static bool at_list_fusion_sensors(void)
{
    ei_syntiant_clear_match();
    ei_built_sensor_fusion_list();
    ei_syntiant_set_match();

    return true;
}

/**
 * @brief 
 * 
 * @param argv 
 * @param argc 
 * @return true 
 * @return false 
 */
static bool at_sample_start(const char **argv, const int argc)
{
    if(argc < 1) {
        ei_printf("Missing sensor name!\n");
        return true;
    }

    const ei_device_sensor_t *sensor_list;
    size_t sensor_list_size;

    pei_device->get_sensor_list((const ei_device_sensor_t **)&sensor_list, &sensor_list_size);

    for (size_t ix = 0; ix < sensor_list_size; ix++) {
        if (strcmp(sensor_list[ix].name, argv[0]) == 0) {
            if (!sensor_list[ix].start_sampling_cb()) {
                ei_printf("ERR: Failed to start sampling\n");
            }
            return true;
        }
    }

    if (ei_connect_fusion_list(argv[0], SENSOR_FORMAT)) {
        if (!ei_fusion_setup_data_sampling()) {
            ei_printf("ERR: Failed to start sensor fusion sampling\n");
        }
    }
    else {
        ei_printf("ERR: Failed to find sensor '%s' in the sensor list\n", argv[0]);
    }


    return true;
}

/**
 * @brief 
 * 
 * @return true 
 * @return false 
 */
static bool at_run_nn_normal(void)
{
    ei_run_nn_normal();

    return ei_run_impulse_is_active();
}

/**
 * @brief 
 * 
 * @return true 
 * @return false 
 */
static bool at_run_nn_normal_cont(void)
{
    ei_run_nn_normal();    

    return ei_run_impulse_is_active();
}

/**
 * @brief 
 * 
 * @return true 
 * @return false 
 */
static bool at_get_mgmt_settings(void)
{
    ei_syntiant_clear_match();
    ei_printf("%s\n", pei_device->get_management_url().c_str());
    ei_syntiant_set_match();

    return true;
}

/**
 * @brief 
 * 
 * @param argv 
 * @param argc 
 * @return true 
 * @return false 
 */
static bool at_set_mgmt_settings(const char **argv, const int argc)
{
    bool ret_val = false;

    if (check_args_num(1, argc) == false) {
        return true;
    }

    if (pei_device != nullptr)
    {
        pei_device->set_management_url(argv[0]);
        ei_printf("OK\n");

        ret_val = true;
    }

    return ret_val;
}

/**
 *
 * @param argv
 * @param argc
 * @return
 */
static bool at_unlink_file(const char **argv, const int argc)
{
    if(argc < 1) {
        ei_printf("Missing argument! Required: " AT_UNLINKFILE_ARGS "\n");
        return false;
    }
    // check if file exist
    std::string filename = argv[0];
    if (pei_device->get_ext_flash()->get_file_exist(filename)){
        //ei_printf("Deleting %s ... \n", filename.c_str());
        if (pei_device->get_ext_flash()->delate_file(filename) == true){
            //ei_printf("File deleted\n", filename.c_str());
            ei_printf("\n");
        }        
    }
    else{
       ei_printf("\n");
    }
    
    return true;
}

/**
 *
 * @param argv
 * @param argc
 * @return
 */
static bool at_read_buffer(const char **argv, const int argc)
{
    bool success = false;

    ei_syntiant_clear_match();

    if(argc < 2) {
        ei_printf("Missing argument! Required: " AT_READBUFFER_ARGS "\n");
        return true;
    }

    if (pei_device != nullptr)
    {
        size_t start = (size_t)atoi(argv[0]);
        size_t length = (size_t)atoi(argv[1]);

        bool use_max_baudrate = false;
        if (argc >= 3 && argv[2][0] == 'y') {
           use_max_baudrate = true;
        }

        if (use_max_baudrate) {
            ei_printf("OK\r\n");
            pei_device->set_max_data_output_baudrate();
            ei_sleep(100);
        }

        success = at_read_encode_send_sample_buffer(start, length);

        if (use_max_baudrate) {
            ei_printf("\r\nOK\r\n");
            ei_sleep(100);
            pei_device->set_default_data_output_baudrate();
            ei_sleep(100);
        }

        if (!success) {
            ei_printf("Failed to read from buffer\n");
        }
        else {
            ei_printf("\n");
        }
    }
    ei_syntiant_set_match();

    return success;
}

/**
 * @brief 
 * 
 * @param argv 
 * @param argc 
 * @return true 
 * @return false 
 */
static bool at_read_raw(const char **argv, const int argc)
{
    ei_syntiant_clear_match();

    if(argc < 2) {
        ei_printf("Missing argument! Required: " AT_READBUFFER_ARGS "\n");
        return true;
    }

    volatile uint32_t start = (uint32_t)atoi(argv[0]);
    volatile uint32_t length = (uint32_t)atoi(argv[1]);

    unsigned char buffer[32];

    for(; (start < length); start += 32)
    {
        pei_device->read_raw(buffer, start, 32);

        int n_display_bytes = (length - start) < 32 ? (length - start) : 32;
        for(int i=0; i<n_display_bytes; i++)
        {
            ei_printf("%.2X ", (unsigned char)buffer[i]);
        }
        ei_printf("\b\r\n");

        if (start > length)
            return true;
    }
    ei_syntiant_set_match();

    return true;
}

/**
 * @brief 
 * 
 * @param start 
 * @param length 
 */
static bool at_read_encode_send_sample_buffer(size_t start, size_t length)
{   
    ei_syntiant_clear_match();
    EiExtFlashMemory *ext_memory = pei_device->get_ext_flash();
    // we are encoiding data into base64, so it needs to be divisible by 3
    const int buffer_size = 513;
    //uint8_t* buffer = (uint8_t*)ei_malloc(buffer_size);
    uint8_t buffer[buffer_size];
    
    start = 0;

    while (1) {
        size_t bytes_to_read = buffer_size;

        if (bytes_to_read > length) {
            bytes_to_read = length;
        }

        if (bytes_to_read == 0) {
            //ei_free(buffer);
            return true;
        }

        uint32_t data_read_temp = ext_memory->read_sample_data(buffer, start, bytes_to_read);

        if (data_read_temp != bytes_to_read) {
            ei_printf("\n[ERR] Error in read sample data!\nstart %ld\nbytes_to_read expected %ld\nData read %ld\n", start, bytes_to_read, data_read_temp);

            return false;                      
        }

        base64_encode((char *)buffer, bytes_to_read, ei_putchar);

        start += bytes_to_read;
        length -= bytes_to_read;
    }

    ei_syntiant_set_match();

    return true;
}

/**
 * @brief 
 * 
 */
static bool at_list_file(void)
{
    ei_printf("File list:\n");
    pei_device->get_ext_flash()->print_file_list();

    return true;
}

/**
 * @brief 
 * 
 * @param argv 
 * @param argc 
 * @return true 
 * @return false 
 */
static bool at_update_file(const char **argv, const int argc)
{
    if(argc < 1) {
        ei_printf("Missing argument! Required: " AT_UNLINKFILE_ARGS "\n");
        return false;
    }

    std::string new_filename = argv[0];
    if (pei_device->get_ext_flash()->get_file_exist(new_filename)){ // if exists, delte it
        ei_printf("Deleting %s ... \n", new_filename.c_str());
        if (pei_device->get_ext_flash()->delate_file(new_filename) == true){
            ei_printf("File deleted\n", new_filename.c_str());
        }        
    }
    // else .. just upload it!
    ei_printf("Ready to update file\n");
    pei_device->wait_flash_model();

    return true;
}

static bool at_format_ext_flash(void)
{
    ei_printf("Formatting ext flash...\n");
    if (pei_device->get_ext_flash()->format_flash() == true){
        ei_printf("Format done!\n");
    }

    return true;
}


static inline bool check_args_num(const int &required, const int &received)
{
    if (received < required) {
        ei_printf("Too few arguments! Required: %d\n", required);
        return false;
    }

    return true;
}
