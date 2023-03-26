from sense_hat import SenseHat

sense = SenseHat()
blue = (0,0,225)
temp = str(int(sense.temperature))
tempF = str(int((sense.temperature * (9/5)) + 32))
sense.show_message(tempF, text_colour=blue)
sense.show_message(temp, text_colour=blue)