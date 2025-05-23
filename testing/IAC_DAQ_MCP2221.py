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

import csv
from datetime import datetime

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

current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_filename = f"Data_Test_{current_time}.csv"
csvfile = open(csv_filename, mode='w', newline='')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(["Elapsed_s", "LoadCell_Raw", "ToF_Raw", "Load_Calibrated_N", "Displacement_mm"])

print("Starting measurements. \n")

start_time = time.time()

# Perform measurements
try:
    while True:
        # Get sensor readings
        loadCellValue = loadCelSensor.read()
        tofValue = tofSensor.range
        
        # 'translate' date to useful values 
        Load = C0_load + C1_load * loadCellValue 
        Tof = C0_tof + C1_tof * tofValue

        elapsed = time.time() - start_time

        # append to the list 
        lst_load += [Load]
        lst_tof += [Tof]
        
        # Get current time
        timestamp = datetime.now().isoformat()

        # Write to CSV
        csvwriter.writerow([elapsed, loadCellValue, tofValue, Load, Tof])
        csvfile.flush()

        # Print to console
        print(f"{elapsed:.3f} [s] | Load cell: {loadCellValue:.2f} [N], Load cell calibrated: {Load:.2f} [N], Distance: {tofValue:.2f} [mm], Distance calibrated: {Tof:.2f} [mm]")
        
        # plot so we can see live what is happening
        plt.clf()
        plt.plot(lst_tof, lst_load, marker='o')
        plt.title('Calibrated Load against calibrated displacement')
        plt.xlabel('Displacement in mm')
        plt.ylabel('Load in N')
        plt.grid(True)
        plt.pause(0.001)
        time.sleep(1)

# Exit
except KeyboardInterrupt:
    print("\nexiting...\n")

finally:
    csvfile.close()