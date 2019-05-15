import serial
import sys
import os
import time
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library  
import platform
from Message import Message
from audio import AudioHendler

COM = '/dev/ttyUSB0'
if platform.system() == 'Windows':
        COM = 'COM4'

ser = serial.Serial(COM,115200)
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

	def begin(self):
                GPIO.add_event_detect(13,GPIO.RISING,callback=self.onClickRecord) # Setup event on pin 12 rising edge

                try:
                        while 1: 
                                if(ser.in_waiting > 0):
                                        line = self.read()
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
                                if self.isAudioTX:
                                        self.isAudioTX = False
                                        if self.count < 2:
                                                aud.record()
                                                self.transmitAudio()
                                        else:
                                                self.count = 0
                except ValueError as e:
                        print str(e)

        def read(self):
                return ser.readline()

        def write(self,message):
                if not self.isAudioTX or not self.isAduioRX:
                        ser.writelines('<SEND>'+'\n'+str(message)+'\n')

        def set_nodeid(self,nodeid):
                ser.writelines('<SET_NODE_ID>'+'\n'+str(nodeid)+'\n')

        def onClickRecord(self,channel):
                self.isAudioTX = True
                self.count = self.count+1

        def transmitAudio(self):
                with open('./media/test.mp3','rb') as f:
                        ser.writelines('<AUDIO>\n')
                        time.sleep(1);
                        byte = f.read(22)
                        ser.write(byte)
                        time.sleep(0.005)
                        while byte != "":
                                byte = f.read(22)
                                ser.write(byte)
                                time.sleep(0.005)
                        ser.write("<END>")
                        print "Finnnniiiiiiisshshhhhh"
                        os.remove('./media/test.mp3')
                        os.remove('./media/test.wav')
