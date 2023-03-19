import sensehat
import sense_hat
from sense_hat import SenseHat
import time

#Temperature Monitoring/Warning System

#variables
Rasp_pi = sensehat.Device()
sense = SenseHat()
#temperature = str(sensehat.Device.get_temperature(Rasp_pi))
temperature = Rasp_pi.temp
#temperature = sense.get_temperature()
baseline = sensehat.baseline
upper_variance = sensehat.upper_variance
lower_variance = sensehat.lower_variance
status = sensehat.status
red = (255,0,0)
green = (0,255,0)
blue = (0,0,225)

#function for resetting main()
def Summary():
    sensehat.main()

#start monitoring system
status = 'start'
#while loop
while status == 'start':
    #if-else to find the correct alert to print

    #Red Alert for temps above upper variance
    if temperature > baseline + upper_variance:
        sense.clear()
        print('RED ALERT: ' + str(int(temperature)) + ' *F')
        sense.show_message('RED ALERT: ' + str(temperature), text_colour=red)

        #Blue Alert for temps below lower variance
    elif temperature < baseline - lower_variance:
        sense.clear()
        print('BLUE ALERT: ' + str(int(temperature)) + ' *F')
        sense.show_message('BLUE ALERT: ' + str(temperature), text_colour=blue)

        #message for temps in safe zone
    else:
        sense.clear()
        print('SAFE: ' + str(int(temperature)) + ' *F')
        sense.show_message('SAFE: ' + str(temperature), text_colour=green)

    #call summary function
    Summary()
    

    #update status to exit loop
    #status = 'end'
