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
#ifndef EI_EXT_FLASH_NICLA_SYNTIANT_H
#define EI_EXT_FLASH_NICLA_SYNTIANT_H

#include "firmware-sdk/ei_device_memory.h"
#include "mbed.h"
#include "SPIFBlockDevice.h"
#include "LittleFileSystem.h"

/**
 * @brief Class to handle the extenral NOR flash
 * @note The externl flash is handled using the lfs filesystem
 * 
 */
class EiExtFlashMemory : public EiDeviceMemory {
public:    
    uint32_t read_sample_data(uint8_t *sample_data, uint32_t address, uint32_t sample_data_size);
    uint32_t write_sample_data(const uint8_t *sample_data, uint32_t address, uint32_t sample_data_size);
    uint32_t erase_sample_data(uint32_t address, uint32_t num_bytes);
    uint32_t get_erase_block_size(void)
    {
        return this->erase_block_size;
    }
    bool get_file_exist(std::string filename);
    void print_file_list(void);
    bool delate_file(std::string filename);
    bool format_flash(void);

protected:
    uint32_t read_data(uint8_t *data, uint32_t address, uint32_t num_bytes);
    uint32_t write_data(const uint8_t *data, uint32_t address, uint32_t num_bytes);
    uint32_t erase_data(uint32_t address, uint32_t num_bytes);
    
public:
    EiExtFlashMemory(void);
    void test_flash(void);
    void init_fs(void);
    void deinit_fs(void);
    
private:
    uint64_t base_address;
    const uint32_t erase_block_size;
    SPIFBlockDevice _spif;
    mbed::LittleFileSystem _lfs;
    bool _fs_is_init;
    const std::string _root_path = "/fs/";
    const std::string _local_file_name = "sample_file.bin";
};

#endif