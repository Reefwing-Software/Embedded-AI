'''
ei uploader for Nicla Voice board
usage:
-s <port> serial port to connect
-f format board 
-p program with missing module
-u force update a single synpgk
'''
import sys
import time
import serial
import logging
import sys
import argparse
import os

AT_COMMAND_LIST_FILES   = "AT+LISTFILES?\r\n"
AT_COMMAND_REMOVEFILE   = "AT+UNLINKFILE="    # mayb not needed ?
AT_COMMAND_UPDATE_MODEL = "AT+UPDATEFILE="
AT_COMMAND_FORMAT_FLASH = "AT+FORMATEXTFLASH\r\n"

required_synpgk = { 'mcu_fw': 0, 'dsp_firmware': 1, 'ei_model': 2}
synpkg_filename = {'mcu_fw_120_v91.synpkg' : 0, 'dsp_firmware_v91.synpkg' : 1, 'ei_model.synpkg' : 2}
synpkg_found = [False, False , False]

def check_match(found_file, file_to_check):
    if found_file.startswith(file_to_check):
        return True
    return False
    
print("Welcome to ei uploader")
port_to_use = ""
flasher_app = ""

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--serial_port", help= "Serial port")
parser.add_argument("-f", help= "Format board", action="store_true")
parser.add_argument("-p", help= "Flash board with missing packages", action="store_true")
parser.add_argument("-u", help= "Force update of package")
parser.add_argument("-a", help= "Uploader")

args = parser.parse_args()
if (len(sys.argv) == 1):
    print("missing arguments")
    exit(1)

port_to_use = args.serial_port
to_format = args.f
flash_board = args.p
anything_to_flash = False
to_force = args.u
flasher_app = args.a

if port_to_use == None:
    print("serial port not specified. Please specify it adding -s <serial_port_to_use>")
    exit(1)

try:
    ser = serial.Serial(port_to_use, 115200, timeout = 0.200)
except serial.SerialException:
    print("Error: Can't open port " + port_to_use)
    exit(1)

print("Port to use: " + port_to_use)

board_found = False
retries = 0
while(board_found == False):
    ser.write(str.encode("test\r\n"))
    str_read = ser.readlines()

    for stringhez in str_read:        
        if (stringhez.decode().startswith("Not a valid AT command (test)")): # the answer starts with this
            print("Board found!")
            ser.readlines()
            board_found = True
            break

    retries += 1
    if retries == 60:
        print("Nicla Voice not answering!")
        exit(2)
    time.sleep(0.5) # give some time


if to_format == True:
    ser.write(str.encode(AT_COMMAND_FORMAT_FLASH))    # format
    print("Formatting....")
    if flash_board == True or to_force != None:
        anything_to_flash = True
        for string, index in required_synpgk.items():
            synpkg_found[index] = False
    str_read = ser.readlines()
    time.sleep(0.5) # give some time 
    str_read = ser.readlines()
    print("Done")

else:
    if flash_board == True or to_force != None:   # if i want to flash the board or i have to force update one model let's check what is present
        anything_to_flash = True
        ser.write(str.encode(AT_COMMAND_LIST_FILES))    # check file list
        # lines_read = 0
        ok_read_cycle = False

        while(True):    # check answers
            str_read = ser.readline().decode()            
            if str_read == "":
                break
            if ">" in str_read and str_read.startswith(">"):    # end of list
                break
            # lines_read+=1
            if (str_read.endswith("File list:\n")): # the answer starts with this
                ok_read_cycle = True
            elif (str_read.endswith(".synpkg\n")):
                print("synpkg found!")
                for string, index in synpkg_filename.items():
                    if check_match(str_read, string) == True:
                        print("Found " + str_read[:len(str_read)-1])
                        synpkg_found[index] = True
        
        if ok_read_cycle == False:  # bad answer from the target
            print("Bad or no answer from the target")
            ser.flush()
            ser.close()
            exit(2)

        for string, index in required_synpgk.items():
            if synpkg_found[index] == False:
                print("Need to flash " + string)

if to_force != None:
    try:
        
        synpkg_found[synpkg_filename[to_force]] = False # force flashing
        print("Force update " + to_force)
        ser.write(str.encode(AT_COMMAND_REMOVEFILE + to_force + "\r\n"))  # remove it 
        str_read = ser.readlines()
        time.sleep(0.5) # give some time 
        str_read = ser.readlines()
        anything_to_flash = True

    except KeyError:
        print("invalid synpkg!")
        exit(3)

def getc(size, timeout = 0.1):
    read_bytes_here = ser.read(size)
    #print("Received: " + str(read_bytes_here))
    return read_bytes_here or None

def putc(data, timeout = 0.1):
    #print("Sending: ", data)
    return ser.write(data) or None  # note that this ignores the timeout

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # enable DEBUG level
logging.basicConfig(stream=sys.stdout, level=logging.INFO) # enable DEBUG level

if anything_to_flash == True:
    file_flashed = 0

    for string, index in synpkg_filename.items():
        if synpkg_found[index] == False:
            ser.flush()
            ser.close()
            ser.port = port_to_use
            ser.baudrate = 115200
            ser.open()

            str_read = ser.flush()            

            found_asnwer = False
            while found_asnwer == False:
                time.sleep(0.25)
                ser.write(str.encode(AT_COMMAND_UPDATE_MODEL + string + "\r\n"))
                time.sleep(0.25)

                for i in range(5):
                    str_read = ser.readline()
                    str_read = str_read.decode()
                    if str_read.__contains__("Ready to update file") == True:
                        print(str_read)
                        found_asnwer = True

            ser.flush()
            ser.close()
            #ser.port = port_to_use
            #ser.baudrate = 230400
            #ser.open()

            # invoke flasher
            cmd = flasher_app + ' send -m "Y" -w "Y" -p ' + port_to_use + ' ' + string
            print(cmd)
            so = os.popen(cmd).read()
            print(so)
            time.sleep(1)
            ser.open()
            time.sleep(1)

    if file_flashed > 0:
        print("Please reset the target to reload the new synpkg")
    else:
        print("Nothing to flash")

print("End of uploader script")
ser.flush()
ser.close()