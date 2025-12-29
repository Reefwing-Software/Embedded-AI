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
#include "ei_inertial.h"
#include "ingestion-sdk-platform/nicla_syntiant/ei_device_syntiant_nicla.h"
#include "edge-impulse-sdk/porting/ei_classifier_porting.h"
#ifdef WITH_IMU
#include "BMI270_Init.h"
/* device class */
#include "NDP.h"
#include "model-parameters/model_metadata.h"

extern NDPClass NDP;

#endif

/* Constant ----------------------------------------------------------------- */
#define GYRO_AS_ACC                 (0) // REMOVE, gyr with same scale as acc

#define ACCELEROMETER_X_LSB         (0x0C)
#define GYRO_X_LSB                  (0x12)
#define MAG_X_LSB                   (0x42)

#define CONVERT_G_TO_MS2            (9.80665f)
#define ACC_RAW_SCALING             (32767.5f)
#define BMI270_CHIP_ID              (0x24)

#define BMM150_CHIP_ID              (0x32)

#define ACC_SCALE_FACTOR            (2.0f*CONVERT_G_TO_MS2)/ACC_RAW_SCALING

#if GYRO_AS_ACC == 1
#define CONVERT_ADC_GYR             ACC_SCALE_FACTOR
#else
#define CONVERT_ADC_GYR             (float)(250.0f/32768.0f)
#endif

#define CONVERT_ADC_MAG_XY          (float)(1300.0f/4096.0f)
#define CONVERT_ADC_MAG_Z           (float)(2500.0f/16384.0f)



#if (GYRO_AS_ACC == 1)
#define NORMALIZE_GYR               (2.0f*CONVERT_G_TO_MS2)
#else
#define NORMALIZE_GYR               (250.0f)
#endif

static bool ei_bmi270_init(void);
static bool ei_inertial_read_accelerometer(float* acc_data);
static bool ei_inertial_read_gyro(float* gyro_data);
static bool ei_inertial_read_mag(float* mag_data);
static float inertial_fusion_data[INERTIAL_AXIS_SAMPLED];

/* Public functions -------------------------------------------------------- */
/**
 * @brief 
 * 
 * @return true 
 * @return false 
 */
bool ei_inertial_init(void)
{
#ifdef WITH_IMU
    if (ei_bmi270_init() == true){
        if(ei_add_sensor_to_fusion_list(inertial_sensor) == false) {
            ei_printf("ERR: failed to register Inertial sensor!\n");
            return false;
        }
    }
    else{
        return false;
    }
#else
    ei_printf("IMU not enabled\n");
#endif
    return true;
}

/**
 *
 * @param n_samples
 * @return
 */
float *ei_fusion_inertial_read_data(int n_samples)
{
    if (n_samples >= 3)
    {
        if (ei_inertial_read_accelerometer(&inertial_fusion_data[0]) == false)
        {
            ei_printf("ERR: no Accel data!\n");
            inertial_fusion_data[0u] = 0.0f;
            inertial_fusion_data[1u] = 0.0f;
            inertial_fusion_data[2u] = 0.0f;
        }
    }

    if (n_samples >= 6)
    {
        if (ei_inertial_read_gyro(&inertial_fusion_data[3u]) == false)
        {
            ei_printf("ERR: no Gyro data!\n");
            inertial_fusion_data[3u] = 0.0f;
            inertial_fusion_data[4u] = 0.0f;
            inertial_fusion_data[5u] = 0.0f;
        }
    }

    if (n_samples == 9)
    {
        if (ei_inertial_read_mag(&inertial_fusion_data[6u]) == false)
        {
            ei_printf("ERR: no Magnetometer data!\n");
            inertial_fusion_data[6u] = 0.0f;
            inertial_fusion_data[7u] = 0.0f;
            inertial_fusion_data[8u] = 0.0f;
        }
    }

    return inertial_fusion_data;
}

#define CHECK_STATUS(s) do { if (s) {ei_printf("SPI access error in line "); ei_printf("%d", __LINE__); for(;;);}} while (0)
/**
 * @brief 
 * 
 */
void ei_inertial_read_test(void)
{
    float acc_data[3] = {0};
    float gyr_data[3] = {0};

    ei_printf("Testing Nicla Voice IMU Sensor");    

    while(1){
        ei_inertial_read_accelerometer(acc_data);
        ei_inertial_read_gyro(gyr_data);

        ei_printf("BMI270 acc data x: %.2f y: %.2f z: %.2f\n", acc_data[0], acc_data[1], acc_data[2]);
        ei_printf("BMI270 gyr data x: %f y: %f z: %f\n", gyr_data[0], gyr_data[1], gyr_data[2]);
        ei_sleep(500);
    }
}

/**
 * @brief 
 * 
 */
static bool ei_bmi270_init(void)
{
#ifdef WITH_IMU
    int s = 0;
    uint8_t __attribute__((aligned(4))) sensor_data[16];
    // Basic master SPI controls
    // 1st read will place the sensor in SPI mode, 2nd read is real read
    s = NDP.sensorBMI270Read(0x0, 1, sensor_data);
    CHECK_STATUS(s);

    s = NDP.sensorBMI270Read(0x0, 1, sensor_data);
    CHECK_STATUS(s);
    ei_printf("BMI270 chip ID is (expected is 0x24): 0x%x\n", sensor_data[0]);    

    bool init = false;

    do {
        // soft reset
        s = NDP.sensorBMI270Write(0x7e, 0x6b);
        CHECK_STATUS(s);
        delay(20); //delay 20ms much longer than reqired 450us

        // back to SPI mode after software reset
        s = NDP.sensorBMI270Read(0x0, 1, sensor_data);
        CHECK_STATUS(s);
        s = NDP.sensorBMI270Read(0x0, 1, sensor_data);
        CHECK_STATUS(s);

        // disable PWR_CONF.adv_power_save
        s = NDP.sensorBMI270Write(0x7c, 0x00);
        CHECK_STATUS(s);
        delay(20); //delay 20ms much longer than reqired 450us

        // prepare config load INIT_CTRL = 0x00
        s = NDP.sensorBMI270Write(0x59, 0x00);
        CHECK_STATUS(s);

        delay(20); //delay 20ms much longer than reqired 450us
        // burst write to INIT_DATA
        ei_printf("BMI270 init starting...");
        s = NDP.sensorBMI270Write(0x5e,
                sizeof(bmi270_maximum_fifo_config_file),
                (uint8_t*)bmi270_maximum_fifo_config_file);
        CHECK_STATUS(s);
        ei_printf("... done!\n");
        delay(20);

        s = NDP.sensorBMI270Write(0x59, 0x01);
        CHECK_STATUS(s);
        delay(200);

        s = NDP.sensorBMI270Read(0x21, 1, sensor_data);
        CHECK_STATUS(s);
        ei_printf("BMI270 Status Register at address 0x21 is (expected is 0x01): 0x%x\n", sensor_data[0]);
        init = (sensor_data[0] == 0x01);
    }while(init == false);

    // configuring device to normal power mode with both Accelerometer and gyroscope working
    s = NDP.sensorBMI270Write(0x7d, 0x0e);
    CHECK_STATUS(s);
    s = NDP.sensorBMI270Write(0x40, 0xa8);
    CHECK_STATUS(s);
    s = NDP.sensorBMI270Write(0x41, 0x00); // +/- 2g
    CHECK_STATUS(s);
    s = NDP.sensorBMI270Write(0x42, 0xa9); // odr 200, OSR2, noise ulp, filter hp
    CHECK_STATUS(s);
    s = NDP.sensorBMI270Write(0x43, 0x11); // gyr range_1000, ois range_2000
    CHECK_STATUS(s);
    s = NDP.sensorBMI270Write(0x7c, 0x02);

    s = NDP.sensorBMM150Write(0x4b, 0x01);
    CHECK_STATUS(s);
    delay(20);
    s = NDP.sensorBMM150Read(0x4b, 1, sensor_data);
    CHECK_STATUS(s);
    ei_printf("BMM150 power control byte at address 0x4B is (expected is 0x01): 0x%x\n", sensor_data[0]);
    
    s = NDP.sensorBMM150Write(0x4c, 0x00);
    CHECK_STATUS(s);

    s = NDP.sensorBMM150Read(0x40, 1, sensor_data);
    CHECK_STATUS(s);
    ei_printf("BMM150 chip ID at address 0x40 is (expected is 0x32): 0x%x\n", sensor_data[0]);
#endif
    return true;
}

/**
 * @brief 
 * 
 * @param acc_data 
 * @return true 
 * @return false 
 */
static bool ei_inertial_read_accelerometer(float* acc_data)
{
#ifdef WITH_IMU
    uint8_t i;
    bool read = false;
    uint8_t __attribute__((aligned(4))) sensor_data[16];

    if (acc_data != nullptr){
        NDP.sensorBMI270Read(ACCELEROMETER_X_LSB, 8, sensor_data);

        for (i = 0; i < 3; i++) {
            acc_data[i] = (float)((int16_t) (sensor_data[i*2] | (sensor_data[i*2 + 1] << 8)));
            acc_data[i] *= ACC_SCALE_FACTOR;
        }

        read = true;
    }

    return read;
#else
    return false;
#endif
}

/**
 * @brief 
 * 
 * @param gyro_data 
 * @return true 
 * @return false 
 */
static bool ei_inertial_read_gyro(float* gyro_data)
{
#ifdef WITH_IMU
    uint8_t i;
    bool read = false;
    uint8_t __attribute__((aligned(4))) sensor_data[16];

    if (gyro_data != nullptr) {
        NDP.sensorBMI270Read(GYRO_X_LSB, 8, sensor_data);

        for (i = 0; i < 3; i++) {
            gyro_data[i] = (float)((int16_t) (sensor_data[i*2] | (sensor_data[i*2 + 1] << 8)));
            gyro_data[i] *= CONVERT_ADC_GYR;            
        }
        
        read = true;
    }

    return read;
#else
    return false;
#endif
}

/**
 * @brief 
 * 
 * @param mag_data 
 * @return true 
 * @return false 
 */
static bool ei_inertial_read_mag(float* mag_data)
{
#ifdef WITH_IMU
    uint16_t i;
    bool read = false;
    uint8_t __attribute__((aligned(4))) sensor_data[16];
    
    if (mag_data != nullptr) {
        NDP.sensorBMM150Read(MAG_X_LSB, 8, sensor_data);
        for (i = 0; i < 3; i++) {
            if (i == 2) {
                mag_data[i] = (float)((int16_t) ((sensor_data[i*2] >> 3) | (sensor_data[i*2 + 1] << 5)));
                mag_data[i] *= CONVERT_ADC_MAG_XY;
            }
            else {
                mag_data[i] = (float)((int16_t) ((sensor_data[i*2] >> 1) | (sensor_data[i*2 + 1] << 7)));
                mag_data[i] *= CONVERT_ADC_MAG_Z;
            }
            // hall we don't read it
            
            // to conversion         
        }

    }

    return read;
#else
    return false;
#endif
}

#ifdef WITH_IMU

static int8_t q7_imu_acc_data[EI_CLASSIFIER_NN_INPUT_FRAME_SIZE];
static uint16_t data_index = 0;
static uint16_t actual_sample = 0;
static bool acc_first = true;

void ei_inertial_prepare_impulse(void)
{
    const char* axes = EI_CLASSIFIER_FUSION_AXES_STRING;
    //q7_imu_acc_data = (int8_t*)ei_malloc(EI_CLASSIFIER_NN_INPUT_FRAME_SIZE);

    if (strstr(axes, "gyr") == axes) {    // ugly, we start with gyr
        acc_first = false;
    }

    if (EI_CLASSIFIER_NN_INPUT_FRAME_SIZE < EI_CLASSIFIER_RAW_SAMPLE_COUNT) {
        ei_printf("Error in the model metadata, EI_CLASSIFIER_NN_INPUT_FRAME_SIZE can't be less than (EI_CLASSIFIER_RAW_SAMPLE_COUNT * EI_CLASSIFIER_RAW_SAMPLES_PER_FRAME)\n");
        while(1){

        };
    }
}

/**
 * @brief 
 * 
 * @param imu_data 
 * @param axes 
 */
void ei_inertial_send_to_ndp(uint8_t axes)
{
    static uint32_t old_time = 0;
    static uint32_t new_time = 0;
    uint32_t i;
    float float_imu_data[6u] = {0};    

    if (q7_imu_acc_data != nullptr) {
        if (actual_sample == 0) {
            memset(q7_imu_acc_data, 0, sizeof(q7_imu_acc_data));
        }

        if (acc_first == true) {
            if (axes >= 3u) {
                ei_inertial_read_accelerometer(float_imu_data);

                for (i = 0; i< 3; i++) {
                    float_imu_data[i] = float_imu_data[i]/( 2.0f*CONVERT_G_TO_MS2 );
                    q7_imu_acc_data[data_index++] = (int8_t)(float_imu_data[i]*128);
                }
            }

            if (axes >= 6u) {
                ei_inertial_read_gyro(&float_imu_data[3]);

                for (i = 3; i< 6; i++) {
                    float_imu_data[i] = float_imu_data[i]/(NORMALIZE_GYR);
                    q7_imu_acc_data[data_index++] = (int8_t)(float_imu_data[i]*128);
                }
            }
        }
        else {
            if (axes >= 6u) {
                ei_inertial_read_gyro(&float_imu_data[3]);

                for (i = 3; i< 6; i++) {
                    float_imu_data[i] = float_imu_data[i]/(NORMALIZE_GYR);
                    q7_imu_acc_data[data_index++] = (int8_t)(float_imu_data[i]*128);
                }
            }

            if (axes >= 3u) {
                ei_inertial_read_accelerometer(float_imu_data);

                for (i = 0; i< 3; i++) {
                    float_imu_data[i] = float_imu_data[i]/(2.0f*CONVERT_G_TO_MS2);
                    q7_imu_acc_data[data_index++] = (int8_t)(float_imu_data[i]*128);
                }
            } 
        }
        
        actual_sample++;
        
        if (actual_sample >= EI_CLASSIFIER_RAW_SAMPLE_COUNT) {
            NDP.sendData((uint8_t*)q7_imu_acc_data, EI_CLASSIFIER_NN_INPUT_FRAME_SIZE);
            actual_sample = 0;
            data_index = 0;            
        }
    }

}
#endif
