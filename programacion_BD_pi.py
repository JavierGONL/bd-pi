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
led_1 = Pin (22, Pin.OUT)
led_2 = Pin (26, Pin.OUT)

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

def movimiento_cabeza(adc_1,adc_2):
    intensidades_luz=[adc_1.read_u16(),adc_2.read_u16()]
    porcentaje_d = intensidades_luz[0]*100/65535
    porcentaje_i = intensidades_luz[1]*100/(65535-500)
    bandera_cambio = abs(intensidades_luz[0] - intensidades_luz[1]) * 100 /65535

    if intensidades_luz[0] >intensidades_luz[1] and bandera_cambio > 10:
        ir_izquierda=False
        ir_derecha=True
        led_1.value(1)
        led_2.value(0)
        return ir_derecha
    if intensidades_luz[0] < intensidades_luz[1] and bandera_cambio > 10:
        ir_derecha=False
        ir_izquierda=True
        led_1.value(0)
        led_2.value(1)
        return ir_derecha
    
    time.sleep(0.5)
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

revoluciones = 10 # 8250 una vuelta
pasos = 0
inicio = True
pos_inicio = True
while True:
    if pos_inicio:
        # movimiento piernas
        while True:
            paso_motor(secuencia2, pins_1, revoluciones,True)
            paso_motor(secuencia2, pins_1, revoluciones,True)
            pasos+=1
            if pasos >= 50:
                pasos = 0
                break
        while True:
            paso_motor(secuencia2, pins_2,revoluciones,True)
            paso_motor(secuencia2, pins_2,revoluciones,True)
            pasos+=1
            if pasos >= 25:
                pasos=0
                break
        while True:
            paso_motor(secuencia2, pins_1, revoluciones)
            paso_motor(secuencia2, pins_1, revoluciones)
            pasos+=1
            if pasos >= 75:
                pasos = 0
                break
        while True:
            paso_motor(secuencia2, pins_2, revoluciones)
            paso_motor(secuencia2, pins_2, revoluciones)
            pasos+=1
            if pasos >= 25:
                pasos=0
                break
        while True:
            paso_motor(secuencia2, pins_1, revoluciones,True)
            paso_motor(secuencia2, pins_1, revoluciones,True)
            pasos+=1
            if pasos >= 25:
                pasos = 0
                break
        # otra pierna
        while True:
            paso_motor(secuencia2, pins_3, revoluciones)
            paso_motor(secuencia2, pins_3, revoluciones)
            pasos+=1
            if pasos >= 50:
                pasos = 0
                break
        while True:
            paso_motor(secuencia2, pins_4, revoluciones)
            paso_motor(secuencia2, pins_4, revoluciones)
            pasos+=1
            if pasos >= 25:
                pasos=0
                break
        while True:
            paso_motor(secuencia2, pins_3, revoluciones,True)
            paso_motor(secuencia2, pins_3, revoluciones,True)
            pasos+=1
            if pasos >= 75:
                pasos = 0
                break
        while True:
            paso_motor(secuencia2, pins_4, revoluciones,True)
            paso_motor(secuencia2, pins_4, revoluciones,True)
            pasos+=1
            if pasos >= 25:
                pasos=0
                break
        while True:
            paso_motor(secuencia2, pins_3, revoluciones)
            paso_motor(secuencia2, pins_3, revoluciones)
            pasos+=1
            if pasos >= 25:
                pasos = 0
                break
        while True: # movimiento de la cabeza
            revolucion_b = 0
            movimiento = movimiento_cabeza(adc_1,adc_2)
            paso_motor(secuencia2, pins_5, revoluciones,movimiento)
            pasos +=1
            if pasos>= 200:
                break
            