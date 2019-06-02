import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library    
import time
from sys import argv
import serial
import pynmea2
#import accl
class GPS:
    def __init__(self):
		self.ser = serial.Serial("/dev/ttyAMA0",9600, timeout = 0.5)

    def collect(self):
        value = 'G:0.0:0.0'
        try:
            while True:
                sentence = self.ser.readline()
                if sentence == "":
                    break
                if sentence.find('GGA') > 0:
                    lat = float(sentence.split(',')[2])/100
                    lon = float(sentence.split(',')[4])/100
                    value = 'G:'+str(lon)+':'+str(lat)
                    break
        except (ValueError, IndexError, serial.SerialException) as e:
            print str(e)
        return value

class ACC:
    def __init__(self):
#        r = accl.accl()
 #       x,y,z = r.get_accl()
        self.x = 12.5
        self.y = 54.23
        self.z = 1440
    

    def collect(self):
        value = 'A:'
        value += str(self.x)
        value += ','
        value += str(self.y)
        value += ','
        value += str(self.z)
        return value


class PULSE:
    def __init__(self):
        self.value=120

    def collect(self):
        value = 'P:'
        value += str(self.value)
        return value


class EMARG:
    def __init__(self):
		self.value = False
		self.setup()

    def setup(self):
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(12,GPIO.RISING,callback=self.listen) # Setup event on pin 12 rising edge
    
    def collect(self):
		  result = 'E:'
		  result += str(self.value)	
		  return result

    def listen(self,channel):
        if self.value != True:
            self.value = True
            time.sleep(60)
            self.value = False
		

