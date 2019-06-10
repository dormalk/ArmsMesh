import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library    
import time
from sys import argv
import serial
import pynmea2
import accl
class GPS:
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyAMA0",9600, timeout = 0.5)
        self.count = 0
    def collect(self):
        value = 'G:0.0:0.0'
        while True:
            sentence = self.ser.readline()
            #print sentence 
            if sentence.find('GGA') > 0:
                lat = float(sentence.split(',')[2])/100
                lon = float(sentence.split(',')[4])/100
                value = 'G:'+str(lon)+':'+str(lat)
                break
            else:
                if self.count > 15:
                    raise ValueError('GPS not detected')
                self.count = self.count + 1
        return value

class ACC:
    def __init__(self):
        self.r = accl.accl()
        
    def collect(self):
        x,y,z = self.r.get_accl()
        value = 'A:'
        value += str(x)
        value += ','
        value += str(y)
        value += ','
        value += str(z)
        #print value
        return value


class PULSE:
    def __init__(self):
        #self.value=120
        self.value = [68,62,65,69,65,61,68,69,64,62,68,63,69,64,65]
        self.arrSize = len(self.value)
        self.index = 0;

    def collect(self):
        value = 'P:'
        value += str(self.value[self.index])
        self.index = self.index + 1
        self.index = self.index % self.arrSize
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
        if not self.value:
            raise ValueError('Emerg not detected')
        return result

    def listen(self,channel):
        if self.value != True:
            self.value = True
            time.sleep(60)
            self.value = False
		

