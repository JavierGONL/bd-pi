from machine import ADC, Pin
import time
adc_1 = ADC(Pin(28))# resistencia izquierda #crear los 2 pines ADC
adc_2= ADC(Pin(27)) # resistencia derecha 
ir_derecha= False
ir_izquierda= False
while True: #inciar el bucle
    intensidades_luz=[adc_1.read_u16(),adc_2.read_u16()]
    print(intensidades_luz)
    if intensidades_luz[0] >intensidades_luz[1]:
        ir_izquierda=False
        ir_derecha=True
        print("derecha") #indicar que la pata que se activa es la derecha
    if intensidades_luz[0] < intensidades_luz[1]:
        ir_derecha=False
        ir_izquierda=True
        print("izquierda")
    time.sleep(0.5)