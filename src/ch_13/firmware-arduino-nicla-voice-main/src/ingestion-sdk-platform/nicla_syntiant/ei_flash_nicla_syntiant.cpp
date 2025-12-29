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
#include "ei_flash_nicla_syntiant.h"
#include "edge-impulse-sdk/porting/ei_classifier_porting.h"

/** 32-bit align write buffer size */
#define WORD_ALIGN(a)	((a & 0x3) ? (a & ~0x3) + 0x4 : a)
/** Align addres to given sector size */
#define SECTOR_ALIGN(a, sec_size)	((a & (sec_size-1)) ? (a & ~(sec_size-1)) + sec_size : a)

/**
 * @brief 
 * 
 */
void EiFlashMemory::test_flash(void)
{
    ei_printf("internl flash size: %ld\n",         memory_size);
    ei_printf("internl flash block size %ld\n",    block_size);
    ei_printf("internl flash config size %ld\n",   config_size);
    ei_printf("internl flash base address %ld\n",   base_address);
    uint32_t _local_block_size = iap.get_sector_size(iap.get_flash_start() + iap.get_flash_size() - 1UL);
    ei_printf("internl flash local block size %ld\n",   _local_block_size);
}

/**
 * @brief 
 * 
 * @param data 
 * @param address 
 * @param num_bytes 
 * @return uint32_t 
 */
uint32_t EiFlashMemory::read_data(uint8_t *data, uint32_t address, uint32_t num_bytes)
{
    int ret;

    ret = iap.read((void *)data, base_address + address, num_bytes);
    if (ret != 0) {
        ei_printf("ERR: Failed to read data! (%d)\n", ret);
        return 0;
    }

    return num_bytes;
}

/**
 * @brief 
 * 
 * @param data 
 * @param address 
 * @param num_bytes 
 * @return uint32_t 
 */
uint32_t EiFlashMemory::write_data(const uint8_t *data, uint32_t address, uint32_t num_bytes)
{
    int ret;

    ret = iap.program(data, WORD_ALIGN(base_address + address), WORD_ALIGN(num_bytes));
    if (ret != 0) {
        ei_printf("ERR: Failed to write data! (%d)\n", ret);
        return 0;
    }

    return num_bytes;
}

/**
 * @brief 
 * 
 * @param address 
 * @param num_bytes 
 * @return uint32_t 
 */
uint32_t EiFlashMemory::erase_data(uint32_t address, uint32_t num_bytes)
{
    int ret;
    
    ret = iap.erase(base_address + address, SECTOR_ALIGN(num_bytes, block_size));

    if(ret != 0) {
        ei_printf("ERR: Failed to erasem flash (%d)\n", ret);
        return 0;
    }

    return num_bytes;
}

/**
 * @brief Construct a new Ei Flash Memory:: Ei Flash Memory object
 * 
 * @param config_size 
 */
EiFlashMemory::EiFlashMemory(uint32_t config_size) 
    : EiDeviceMemory(config_size, 90, 0, 4096)
{    
    iap.init();

    uint32_t _local_block_size = iap.get_sector_size(iap.get_flash_start() + iap.get_flash_size() - 1UL);

	//block_size = iap.get_sector_size(iap.get_flash_start() + iap.get_flash_size() - 1UL);
    memory_size = iap.get_flash_size();
    used_blocks = (config_size < _local_block_size) ? 1 : ceil(float(config_size) / _local_block_size);
    memory_blocks = memory_size / _local_block_size;
    base_address = SECTOR_ALIGN(FLASHIAP_APP_ROM_END_ADDR, _local_block_size);
}
