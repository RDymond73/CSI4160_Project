import sensehat
import sense_hat
from sense_hat import SenseHat

#Temperature Monitoring/Warning System

#variables
Rasp_pi = sensehat.Device()
sense = SenseHat()
#temperature = str(sensehat.Device.get_temperature(Rasp_pi))
temperature = str(sensehat.Device.get_temperature)
baseline = sensehat.baseline
upper_variance = sensehat.upper_variance
lower_variance = sensehat.lower_variance
status = sensehat.status
red = (255,0,0)
green = (0,255,0)

status = 'start'
while status == 'start':
    sensehat.main()
    print(temperature)
    sense.clear(red)
    sense.show_message(temperature, text_colour=red)
    status = 'end'