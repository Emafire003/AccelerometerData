# Orginal Author: peppe8o
# Blog: https://peppe8o.com
# Date: Aug 25th, 2021

# Edited and Maintained by: Emafire003
# Github: https://github.com/Emafire003
# Date 30/11/2022

# Version: 0.1

from imu import MPU6050
import time
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

ax_base, ay_base, az_base, gx_base, gy_base, gz_base = -1
stabilized_values = False


def stabilize_values():
    axs = [round(imu.accel.x, 2)]
    ays = [round(imu.accel.y, 2)]
    azs = [round(imu.accel.z, 2)]
    gxs = [round(imu.gyro.x)]
    gys = [round(imu.gyro.y)]
    gzs = [round(imu.gyro.z)]
    for i in 20:
        axs.append(round(imu.accel.x, 2))
        ays.append(round(imu.accel.y, 2))
        azs.append(round(imu.accel.z, 2))
        gxs.append(round(imu.gyro.x))
        gys.append(round(imu.gyro.y))
        gzs.append(round(imu.gyro.z))
        time.sleep(0.5)

    return get_average(axs), get_average(ays), get_average(azs), get_average(gxs), get_average(gys), get_average(gzs)


def get_average(list_of_stuff):
    sum_of_stuff = 0
    for i in len(list_of_stuff):
        sum_of_stuff = sum_of_stuff + list_of_stuff[i]
    return sum_of_stuff / len(list_of_stuff)


print("Do you want to stabilize the values? y/n")

if input() == "y":
    print("Calibrating... DO NOT MOVE THE ACCELEROMETER UNTIL THIS PHASE IS COMPLETED")
    print("This should be done in 10s")
    ax_base, ay_base, az_base, gx_base, gy_base, gz_base = stabilize_values()
    print("Done calibrating, the baseline values are: ")
    print("bAx: ", ax_base, "\t", "bAy: ", ay_base, "\t", "bAx: ", az_base, "\t", "bGx: ", gx_base, "\t", "bGy: ", gy_base, "\t", "bGz: ", gz_base, "\t", "        ", end="\r")
    stabilized_values = True

while True:
    # Following print shows original data get from libary. You can uncomment to see raw data
    print("Raw data: ")
    print(imu.accel.xyz, imu.gyro.xyz, imu.temperature, end='\r')

    # Following rows round values get for a more pretty print:
    ax = round(imu.accel.x, 2)
    ay = round(imu.accel.y, 2)
    az = round(imu.accel.z, 2)
    gx = round(imu.gyro.x)
    gy = round(imu.gyro.y)
    gz = round(imu.gyro.z)
    tem = round(imu.temperature, 2)

    if stabilized_values:
        print("Stabilized values:")
        ax = ax - ax_base
        ay = ay - ay_base
        az = az - az_base
        gx = gx - gx_base
        gy = gy - gy_base
        gz = gz - gz_base

    print("Ax: ", ax, "\t", "Ay: ", ay, "\t", "Ax: ", az, "\t", "Gx: ", gx, "\t", "Gy: ", gy, "\t", "Gz: ", gz, "\t",
          "temp: ", tem, "        ", end="\r")

    # Following sleep statement makes values enought stable to be seen and
    # read by a human from shell
    time.sleep(0.2)
