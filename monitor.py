import sensehat
import sense_hat
from sense_hat import SenseHat
import time

#Temperature Monitoring/Warning System

#function for resetting main()
def Summary(alert):
    sensehat.main(alert)

#variables
Rasp_pi = sensehat.Device()
sense = SenseHat()
summary = sensehat.main('alert')
temperature = sensehat.convert(int(Rasp_pi.temp))
baseline = int(summary[0])
upper_variance = int(summary[1])
lower_variance = int(summary[2])
status = Rasp_pi.status
red = (255,0,0)
green = (0,255,0)
blue = (0,0,225)

#start monitoring system
#while loop
while status == 'running':
    #if-else to find the correct alert to print

    #Red Alert for temps above upper variance
    if  baseline + upper_variance + lower_variance == 0:
        sense.clear()
        print('Gathering Data')
        sense.show_message('Gathering Data')
        summary = sensehat.main('alert')
        baseline = int(summary[0])
        upper_variance = int(summary[1])
        lower_variance = int(summary[2])
        Summary('Gathering Data')
    if temperature > baseline + upper_variance:
        sense.clear()
        print('RED ALERT: ' + str(int(temperature)) + ' *F')
        sense.show_message('RED ALERT: ' + str(int(temperature)) + ' *F', text_colour=red)
        summary = sensehat.main('alert')
        baseline = int(summary[0])
        upper_variance = int(summary[1])
        lower_variance = int(summary[2])
        print(baseline)
        print(upper_variance)
        print(lower_variance)
        Summary('RED ALERT')

        #Blue Alert for temps below lower variance
    elif temperature < baseline - lower_variance:
        sense.clear()
        print('BLUE ALERT: ' + str(int(temperature)) + ' *F')
        sense.show_message('BLUE ALERT: ' + str(int(temperature) + ' *F'), text_colour=blue)
        summary = sensehat.main('alert')
        baseline = int(summary[0])
        upper_variance = int(summary[1])
        lower_variance = int(summary[2])
        Summary('BLUE ALERT')

        #message for temps in safe zone
    else:
        sense.clear()
        print('SAFE: ' + str(int(temperature)) + ' *F')
        sense.show_message('SAFE: ' + str(int(temperature)) + ' *F', text_colour=green)
        summary = sensehat.main('alert')
        baseline = int(summary[0])
        upper_variance = int(summary[1])
        lower_variance = int(summary[2])
        Summary('SAFE')
