import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library    
import time
from sys import argv
import serial
import pynmea2
from pulsesensor import Pulsesensor

class GPS:
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyAMA0",115200, timeout = 0.5)

    def collect(self):
        value = 'G:0.0:0.0'
        while True:
            sentence = self.ser.readline()
            if sentence == "":
                break
                print sentence
            if sentence.find('GGA') > 0:
                lat = float(sentence.split(',')[2])/100
                lon = float(sentence.split(',')[4])/100
                value = 'G:'+str(lon)+':'+str(lat)
                break
        return value

class ACC:
    def __init__(self):
        self.x = 1.12
        self.y = 3.12
        self.z = 5.00

    def collect(self):
        value = 'A:'
        value += str(self.x)
        value += ':'
        value += str(self.y)
        value += ':'
        value += str(self.z)
        return value


class PULSE:
    def __init__(self):
        self.p = Pulsesensor()
        self.p.startAsyncBPM()

    def collect(self):
        value = 'P:'
        value += str(self.p.BPM)
        if self.p.BPM <= 0:
            raise ValueError('BPM not detect')
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
                    raise ValueError('Emeg not detect')
        return result

    def listen(self,channel):
        if self.value != True:
            self.value = True
            time.sleep(30)
            self.value = False
		

