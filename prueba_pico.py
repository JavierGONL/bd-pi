import machine 
import utime  
led_externo = machine.Pin('LED', machine.Pin.OUT) 

while True:     
   led_externo.value(0)         
   utime.sleep(2)     
   led_externo.value(1) 