#imports
from machine import ADC, Pin, I2C
from micropython_bmi160 import bmi160
import time
import socket
#import sys
#boot.py
#primero se ejecuta el boot para conectarlo a wifi
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('Bidipi', 'michi111')

while not wlan.isconnected() and wlan.status() >= 0:
    print("Conectando...")
    if wlan.isconnected():
        break
print(wlan.ifconfig())

html = """<!DOCTYPE html>
<html>
<head> <title> Gatito </title> </head>
<body>
</body>
</html>
"""

# pines motores

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

#crear los 2 pines ADC y los leds
adc_1 = ADC(Pin(27))# resistencia izquierda
adc_2= ADC(Pin(28)) # resistencia derecha
led_1 = Pin (22, Pin.OUT)
led_2 = Pin (26, Pin.OUT)
# banderas
ir_derecha= False
ir_izquierda= False

#giroscopio
i2c = I2C(1, sda=Pin(18), scl=Pin(19))  # Correct I2C pins for RP2040
bmi = bmi160.BMI160(i2c)
bandera_equilibrio=False

#pasos motores

secuencia = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
    ]

secuencia2 = [
    [1,1,0,0],
    [0,1,1,0],
    [0,0,1,1],
    [1,0,0,1]
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

#programacion motores
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

def giroscopio(bmi = bmi,bandera_equilibrio = bandera_equilibrio):
    while True:
        gyrox, gyroy, gyroz = bmi.gyro
        #print(f"x:{gyrox:.2f}°/s, y:{gyroy:.2f}°/s, z{gyroz:.2f}°/s") #monitoreo
        if abs(gyrox) >=12 or abs(gyroy)>=12:
            bandera_equilibrio=True
        time.sleep(0.5)
        break
    while bandera_equilibrio:
        pasos=0
        while pasos <=100:
            doble_paso_motor(secuencia2,pins_1,pins_2,13.75,False)
            doble_paso_motor(secuencia2,pins_3,pins_4,13.75,True)
            pasos+=1
        pasos=0
        break


# funcion que calcula donde girar la cabeza
def movimiento_cabeza(adc_1,adc_2):
    intensidades_luz=[adc_1.read_u16(),adc_2.read_u16()]
    # porcentaje_d = intensidades_luz[0]*100/65535
    # porcentaje_i = intensidades_luz[1]*100/(65535-500)
    bandera_cambio = abs(intensidades_luz[0] - intensidades_luz[1]) * 100 /65535
    if intensidades_luz[0] >intensidades_luz[1] and bandera_cambio > 10:
        ir_derecha=True
        led_1.value(1)
        led_2.value(0)
        return ir_derecha
    if intensidades_luz[0] < intensidades_luz[1] and bandera_cambio > 10:
        ir_derecha=False
        led_1.value(0)
        led_2.value(1)
        return ir_derecha

#Aqui va el codigo para conectarlo a Wifi

revoluciones = 10 # 8250 una vuelta
pasos = 0


def Caminar():
    global revoluciones
    global pasos
    print("gatito")
    print(revoluciones)
    print(pasos)
    while True:
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
            
def PiernaIzquierda():
    global revoluciones
    global pasos
    while True:
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
def PiernaDerecha():
    # otra pierna
    global revoluciones
    global pasos
    while True:
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
def Cabeza():
    global revoluciones
    global pasos
    while True: # movimiento de la cabeza
            revolucion_b = 0
            movimiento = movimiento_cabeza(adc_1,adc_2)
            paso_motor(secuencia2, pins_5, revoluciones,movimiento)
            pasos +=1
            if pasos>= 500:
                break
                
def simulacion():
    global revoluciones
    global pasos
    pos_inicio = True
    while True:
        if pos_inicio:
            # movimiento piernas
            while True:
                movimiento = movimiento_cabeza(adc_1,adc_2)
                paso_motor(secuencia2, pins_1, revoluciones,True)
                paso_motor(secuencia2, pins_5, revoluciones,movimiento)
                paso_motor(secuencia2, pins_1, revoluciones,True)
                pasos+=1
                if pasos >= 50:
                    pasos = 0
                    break
            while True:
                movimiento = movimiento_cabeza(adc_1,adc_2)
                paso_motor(secuencia2, pins_2,revoluciones,True)
                paso_motor(secuencia2, pins_2,revoluciones,True)
                pasos+=1
                if pasos >= 25:
                    pasos=0
                    break
            while True:
                movimiento = movimiento_cabeza(adc_1,adc_2)
                paso_motor(secuencia2, pins_1, revoluciones)
                paso_motor(secuencia2, pins_1, revoluciones)
                pasos+=1
                if pasos >= 75:
                    pasos = 0
                    break
            while True:
                movimiento = movimiento_cabeza(adc_1,adc_2)
                paso_motor(secuencia2, pins_2, revoluciones)
                paso_motor(secuencia2, pins_2, revoluciones)
                pasos+=1
                if pasos >= 25:
                    pasos=0
                    break
            while True:
                movimiento = movimiento_cabeza(adc_1,adc_2)
                paso_motor(secuencia2, pins_1, revoluciones,True)
                paso_motor(secuencia2, pins_1, revoluciones,True)
                pasos+=1
                if pasos >= 25:
                    pasos = 0
                    break
            # otra pierna
            while True:
                movimiento = movimiento_cabeza(adc_1,adc_2)
                paso_motor(secuencia2, pins_3, revoluciones)
                paso_motor(secuencia2, pins_3, revoluciones)
                pasos+=1
                if pasos >= 50:
                    pasos = 0
                    break
            while True:
                movimiento = movimiento_cabeza(adc_1,adc_2)
                paso_motor(secuencia2, pins_4, revoluciones)
                paso_motor(secuencia2, pins_4, revoluciones)
                pasos+=1
                if pasos >= 25:
                    pasos=0
                    break
            while True:
                movimiento = movimiento_cabeza(adc_1,adc_2)
                paso_motor(secuencia2, pins_3, revoluciones,True)
                paso_motor(secuencia2, pins_3, revoluciones,True)
                pasos+=1
                if pasos >= 75:
                    pasos = 0
                    break
            while True:
                movimiento = movimiento_cabeza(adc_1,adc_2)
                paso_motor(secuencia2, pins_4, revoluciones,True)
                paso_motor(secuencia2, pins_4, revoluciones,True)
                pasos+=1
                if pasos >= 25:
                    pasos=0
                    break
            while True:
                movimiento = movimiento_cabeza(adc_1,adc_2)
                paso_motor(secuencia2, pins_3, revoluciones)
                paso_motor(secuencia2, pins_3, revoluciones)
                pasos+=1
                if pasos >= 25:
                    pasos = 0
                    break
            
"""
def SolicitudWeb(conn):
    request= conn.recv(1024)  # Recibe la solicitud HTTP
    request = request.decode('utf-8')
    print("Solicitud recibida:")
    print(request)

    if "/caminar" in request:
        Caminar()
        response = "HTTP/1.1 200 OK\n\nCaminar."
    elif "/piernaizquierda" in request:
       PiernaIzquierda()
       response = "HTTP/1.1 200 OK\n\nPierna izquierda."
    elif "/piernaderecha" in request:
        PiernaDerecha()
        response = "HTTP/1.1 200 OK\n\nPierna derecha."
    elif "/cabeza" in request:
        Cabeza()
        response = "HTTP/1.1 200 OK\n\nCabeza."
    else:
        response = "HTTP/1.1 404 Not Found\n\n404 Not Found."

    conn.send(response)
    conn.close()
    
addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

while True:
    cl, addr = s.accept()  
    print('Cliente conectado desde', addr)
    SolicitudWeb(cl)
    """
def SolicitudWeb(conn):
    try:
        requests = conn.recv(1024)
        print("Solicitud recibida:")
        request=requests.decode("utf-8")
        print(request)

        if b"/caminar" in request:
            Caminar()
            response = "HTTP/1.1 200 OK\n\nCaminar."
        elif b"/piernaizquierda" in request:
            PiernaIzquierda()
            response = "HTTP/1.1 200 OK\n\nPierna izquierda."
        elif b"/piernaderecha" in request:
            PiernaDerecha()
            response = "HTTP/1.1 200 OK\n\nPierna derecha."
        elif b"/cabeza" in request:
            Cabeza()
            response = "HTTP/1.1 200 OK\n\nCabeza."
        else:
            response = "HTTP/1.1 404 Not Found\n\n404 Not Found."

        conn.send(response.encode())
    finally:
        conn.close()

addr = socket.getaddrinfo('192.168.181.149', 8080)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print(addr)
while True:
    try:
        cl, addr = s.accept()
        print(cl)
        print('Cliente conectado desde', addr)
        SolicitudWeb(cl)
    except Exception as e:
        print(f"Error: {e}")


