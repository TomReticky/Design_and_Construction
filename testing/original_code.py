# Just in case the environment variables were not properly set
import os
os.environ["BLINKA_MCP2221"] = "1"
os.environ["BLINKA_MCP2221_RESET_DELAY"] = "-1"

import board
import busio
import time
import matplotlib.pyplot as plt

import adafruit_vl53l0x
from cedargrove_nau7802 import NAU7802

# Load cell
loadCelSensor = NAU7802(board.I2C(), address=0x2a, active_channels=1)

# Time of flight sensor
i2c = busio.I2C(board.SCL, board.SDA)
tofSensor = adafruit_vl53l0x.VL53L0X(i2c)

# Constants to be determined during calibration
C0_load = 0
C1_load = 1
C0_tof = 0
C1_tof = 1

# generate empty lists to enable plotting during the test 
lst_load = [] # List to store load cell values
lst_tof = [] # List to store load cell values

print("Starting measurements. \n")

# Perform measurements
try:
    while True:
        # Get sensor readings
        loadCellValue = loadCelSensor.read()
        tofValue = tofSensor.range

        # Output sensor data
        # print to screen
        print("Load cell: {:.0f}, Distance: {:.0f}".format(loadCellValue, tofValue))
        # print("Load cell: {:.0f}".format(loadCellValue))
        # save to file (during test, not afterwards), and these are the raw data 
        file2write=open("Data_Test_CHANGENAME.txt",'a')
        file2write.write(str(loadCellValue) + " " + str(tofValue) + "\n")
        file2write.flush()
        file2write.close()
        
        # 'translate' date to useful values 
        Load = C0_load + C1_load * loadCellValue 
        Tof = C0_tof + C1_tof * tofValue 
        
        # append to the list 
        lst_load += [Load]
        lst_tof += [Tof]
        
        # plot so we can see live what is happening
        plt.plot(lst_tof, lst_load)
        plt.title('Load against displacement')
        plt.xlabel('Displacement in mm')
        plt.ylabel('Load in N')
        plt.draw()
        plt.pause(0.001)
        time.sleep(1)

# Exit
except KeyboardInterrupt:
    print("\nexiting...\n")
