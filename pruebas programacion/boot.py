#boot.py
#primero se ejecuta el boot para conectarlo a wifi
import network
import time
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('Wifi', 'contraseña')

while not wlan.isconnected() and wlan.status() >= 0:
    print("Conectando...")
    if wlan.isconnected():
        break
print(wlan.ifconfig())
time.sleep(5)
#instale boot.py si desea poder reconfigurar la pi pico w posteriormente
#si solo instala main.py, la pico posteriormente no se dejará conectar al pc
#en dado caso, la solución es formatear la memoria de la pi pico w