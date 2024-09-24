from machine import ADC, Pin
import time


#
# giroscopio
# motores

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
# motor cabeza

pins_5=[
     Pin (12, Pin.OUT), # IN1
     Pin (13, Pin.OUT), # IN2
     Pin (14, Pin.OUT), # IN3
     Pin (15, Pin.OUT)  # IN4
     ]
# cabeza
adc_1 = ADC(Pin(27))# resistencia izquierda #crear los 2 pines ADC
adc_2= ADC(Pin(28)) # resistencia derecha 
ir_derecha= False
ir_izquierda= False

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


def paso_motor(secuencia, pins, revoluciones,invertir =False):
    revolucion_a = 0
    while True:
        if not invertir:
            for paso in secuencia:
                for i in range(len(pins)):
                    pins[i].value(paso[::-1][i])
                    time.sleep(0.001)
                    revolucion_a +=1
            if revolucion_a >= revoluciones:             
                break
        else: 
            for paso in secuencia:
                for i in range(len(pins)):
                    pins[i].value(paso[i])
                    time.sleep(0.001)
                    revolucion_a +=1
            if revolucion_a >= revoluciones:             
                break
def doble_paso_motor(secuencia, pins, pins2, revoluciones,invertir=False):# esta función mueve 2 motores a la vez
    revolucion_a = 0
    while True:
        if not invertir:
            for paso in secuencia:
                for i in range(len(pins)):
                    pins[i].value(paso[i])
                    pins2[i].value(paso[i])
                    time.sleep(0.001)
                    revolucion_a +=1
            if revolucion_a >= revoluciones:             
                break
        else: 
            for paso in secuencia:
                for i in range(len(pins)):
                    pins[i].value(paso[::-1][i])
                    pins2[i].value(paso[::-1][i])
                    time.sleep(0.001)
                    revolucion_a +=1
            if revolucion_a >= revoluciones:             
                break

revoluciones = 10 # 8250 una vuelta
pasos = 0
inicio = True
pos_inicio = True
"""
while True:
    paso_motor(secuencia2, pins_1, revoluciones,True)
    paso_motor(secuencia2, pins_1, revoluciones,True)
    pasos+=1
    if pasos >= 256:
    # 256 pasos es una vuelta entera bajo este programa, así que cada paso equivale a la activación de 2 fases del motor
        pasos = 0
        break

"""

