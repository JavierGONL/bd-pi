from machine import ADC, Pin
import time


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
    
revoluciones = 10 # 8250 una vuelta
pasos = 0
inicio = True
pos_inicio = True
while True:
    if pos_inicio:    
        while True: # movimiento de la cabeza
                revolucion_b = 0
                movimiento = movimiento_cabeza(adc_1,adc_2)
                paso_motor(secuencia2, pins_5, revoluciones,movimiento)
                pasos +=1
                if pasos>= 200:
                    break