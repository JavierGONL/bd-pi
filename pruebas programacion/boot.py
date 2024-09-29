#boot.py
#ignorar este archivo, la función de boot está incluida en main.py
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
