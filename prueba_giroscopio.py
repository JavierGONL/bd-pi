# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
from machine import Pin, I2C
from micropython_bmi160 import bmi160
from prueba_motores import *
i2c = I2C(1, sda=Pin(18), scl=Pin(19))  # Correct I2C pins for RP2040
bmi = bmi160.BMI160(i2c)
bandera_equilibrio=False
def giroscopio(bmi,bandera_equilibrio):
    while True:
        gyrox, gyroy, gyroz = bmi.gyro
        #print(f"x:{gyrox:.2f}°/s, y:{gyroy:.2f}°/s, z{gyroz:.2f}°/s")
        if abs(gyrox) >=12 or abs(gyroy)>=12:
            bandera_equilibrio=True
        time.sleep(0.5)
        return bandera_equilibrio
if __name__=="__main__":
    while True: #monitoreo del programa
        if giroscopio(bmi,bandera_equilibrio)==True:
            paso_motor(secuencia2,pins_1,revoluciones,True)
            

