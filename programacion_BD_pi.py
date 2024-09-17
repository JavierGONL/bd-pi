from machine import Pin
import time


pins_1= [
     Pin (0, Pin.OUT), # IN1
     Pin (1, Pin.OUT), # IN2
     Pin (2, Pin.OUT), # IN3
     Pin (3, Pin.OUT)  # IN4
     ]
pins_2=[
     Pin (4, Pin.OUT), # IN1
     Pin (5, Pin.OUT), # IN2
     Pin (6, Pin.OUT), # IN3
     Pin (7, Pin.OUT)  # IN4
     ]
pins_3=[
     Pin (8, Pin.OUT), # IN1
     Pin (9, Pin.OUT), # IN2
     Pin (10, Pin.OUT), # IN3
     Pin (11, Pin.OUT)  # IN4
     ]
pins_4=[
     Pin (16, Pin.OUT), # IN1
     Pin (17, Pin.OUT), # IN2
     Pin (20, Pin.OUT), # IN3
     Pin (21, Pin.OUT)  # IN4
     ]


secuencia = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
    ]
secuencia_invertida =[
    [0,0,0,1],
    [0,0,1,0],
    [0,1,0,0],
    [1,0,0,0]
    ]

secuencia2 = [
    [1,1,0,0],
    [0,1,1,0],
    [0,0,1,1],
    [1,0,0,1]
    ]

secouencia2_invertida = [
    [1,0,0,1],
    [0,0,1,1],
    [0,1,1,0],
    [1,1,0,0]
    ]

secuencia3 = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [1,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
    ]

secuencia3_invertida = [
    [1,0,0,1],
    [0,0,0,1],
    [0,0,1,1],
    [0,1,1,1],
    [0,1,0,0],
    [1,1,0,0],
    [1,0,0,0],
    [1,0,1,0]
    ]

def paso_motor(secuencia, pins, revoluciones):
    revolucion_a = 0
    while True:
        for paso in secuencia:
            for i in range(len(pins)):
                pins[i].value(paso[i])
                time.sleep(0.001)
                revolucion_a +=1
        if revolucion_a >= revoluciones:             
            break

def doble_paso_motor(secuencia, pins, pins2, revoluciones,invertir=False):
    revolucion_a = 0
    while True:
        if not invertir:
            for paso in secuencia:
                for i in range(len(pins)):
                    pins[i].value(paso[::-1][i])
                    pins2[i].value(paso[i])
                    time.sleep(0.001)
                    revolucion_a +=1
            if revolucion_a >= revoluciones:             
                break
        else: 
            for paso in secuencia:
                for i in range(len(pins)):
                    pins[i].value(paso[i])
                    pins2[i].value(paso[::-1][i])
                    time.sleep(0.001)
                    revolucion_a +=1
            if revolucion_a >= revoluciones:             
                break
    
def cuadruple_paso_motor(secuencia, pins1, pins2, pins3, pins4, revoluciones, invertir=False):
    revolucion_a = 0
    while True:
        if not invertir:
            for paso in secuencia:
                for i in range(len(pins)):
                    pins1[i].value(paso[::-1][i])
                    pins2[i].value(paso[i])
                    pins3[i].value(paso[i])
                    pins4[i].value(paso[::-1][i])
                    time.sleep(0.001)
                    revolucion_a +=1
            if revolucion_a >= revoluciones:             
                break
        else: 
            for paso in secuencia:
                for i in range(len(pins)):
                    pins1[i].value(paso[i])
                    pins2[i].value(paso[::-1][i])
                    pins3[i].value(paso[::-1][i])
                    pins4[i].value(paso[i])
                    time.sleep(0.001)
                    revolucion_a +=1
            if revolucion_a >= revoluciones:             
                break

revoluciones = 1250 # 8250 una vuelta
pasos = 0
inicio = True
pos_inicio = True
while True:
    if pos_inicio:
        while True:
            cuadruple_paso_motor(secuencia3, pins_1, pins_2, pins_3, pins_4, 2000)