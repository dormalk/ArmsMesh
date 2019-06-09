import serial
import sys
import os
import time
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library  
import platform
from Message import Message
from audio import AudioHendler
from playsound import playsound

COM = '/dev/ttyUSB0'
if platform.system() == 'Windows':
        COM = 'COM4'
	
aud = AudioHendler()


class RFBridge:
        def __init__(self,nodeid,redisTool):
                self.nodeid = nodeid
                self.redisTool = redisTool
                GPIO.setwarnings(False) # Ignore warning for now
                GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
                GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                self.isAduioRX = False
                self.isAudioTX = False
                self.count = 0
                while True:
                        try:
                                self.ser = serial.Serial(COM,115200)
                                break
                        except serial.SerialException as e:
                                print e
                                time.sleep(1)
		
	def begin(self):
                GPIO.add_event_detect(13,GPIO.RISING,callback=self.onClickRecord) # Setup event on pin 12 rising edge

                while True:
                                try:
                                        if(self.ser.in_waiting > 0):
                                                line = self.read()
                                                print line
                                                        #line is 1 line from the recived message and not all the message
                                                        #here we need to check which tag we read and build full message and push it to redis
                                                        #we can be sure that the message is for current RespB coz arduino handle this issue
                                                        #print line
                                                if line == '<START>':
                                                        self.set_nodeid(self.nodeid)  
                                                if '<NEW_MSG>' in line:
                                                        message = Message()
                                                        message.set_msg_id(self.read()[9:])
                                                        message.set_time(self.read()[12:])
                                                        message.set_src(src = self.read()[6:])
                                                        message.set_data(self.read()[7:])
                                                        # print message.get_message()
                                                                # message.get_message() push to redis
                                                if '<AUDIO_DATA>' in line:
                                                        self.recivedAudio()
                                                
                                                        
                                                        
                                except ValueError as e:
                                        print str(e)
                                except serial.SerialException as e:
                                        while True:
                                                try:
                                                        self.ser = serial.Serial(COM,115200)
                                                        break
                                                except serial.SerialException as e:
                                                        time.sleep(0.5)
                                                        print str(e)
                                except:
                                        self.ser = serial.Serial(COM,115200)
					
        def read(self):
                return self.ser.readline()

        def write(self,message):
                try:
                        if not self.isAudioTX and not self.isAduioRX:
                                self.ser.writelines('<SEND>'+'\n'+str(message)+'\n')
                except serial.serialutil.SerialException as e:
                        print str(e)
                        
        def set_nodeid(self,nodeid):
                self.ser.writelines('<SET_NODE_ID>'+'\n'+str(nodeid)+'\n')

        def onClickRecord(self,channel):
                self.isAudioTX = True
                aud.record()
                self.transmitAudio()        

        def transmitAudio(self):
                with open('./media/test.mp3','rb') as f:
                        self.ser.writelines('<AUDIO>\n')
                        time.sleep(1)
                        byte = f.read(22)
                        self.ser.write(byte)
                        time.sleep(0.02)
                        while byte != "":
                            byte = f.read(22)
                            self.ser.write(byte)
                            time.sleep(0.02)
                        time.sleep(1)
                        self.isAudioTX = False
                        
        def recivedAudio(self):
                self.isAduioRX = True
                try:
                        os.remove('/home/dor/Desktop/ArmsMesh/RespMesh/media/test.mp3')
                except:
                        print "just error"
                curr = 0
                print "START"
                with open('./media/test.mp3','ab') as f2:
                        while not (self.ser.in_waiting > 0):
                                continue
                        f2.write(self.ser.read(22))
                        while True:
                                if(self.ser.in_waiting > 0):
                                        row = self.ser.readline()
                                        print "first"+row
                                        if "<AUDIO_DATA>" in row:
                                                curr = time.time()
                                                row = self.ser.read(22)
                                                print "sec"+row
                                                if "REC" in row:
                                                        self.ser.write("<END_AUDIO>")
                                                        break
                                                f2.write(row)
                                        if "<DATA>" in row:
                                                self.ser.write("<END_AUDIO>")
                                                break
                self.isAduioRX = False
                #playsound("./media/test.mp3")
                pi = "/home/dor/Desktop/ArmsMesh/RespMesh/media/test.mp3"
                os.system("mpg123 "+pi)
                time.sleep(1)
