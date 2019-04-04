import serial
import sys
import platform
from Message import Message

COM = '/dev/ttyUSB0'
if platform.system() == 'Windows':
        COM = 'COM4'

ser = serial.Serial(COM,115200)

class RFBridge:
        def __init__(self,nodeid,redisTool):
                self.nodeid = nodeid
                self.redisTool = redisTool

	def begin(self):
                while 1:                                
                        if(ser.in_waiting > 0):
                                line = self.read()
                                #line is 1 line from the recived message and not all the message
                                #here we need to check which tag we read and build full message and push it to redis
                                #we can be sure that the message is for current RespB coz arduino handle this issue
                                print line
                                if line == '<START>':
                                        self.set_nodeid(self.nodeid)  
                                if '<NEW_MSG>' in line:
                                        message = Message()
                                        message.set_msg_id(self.read()[9:])
                                        message.set_time(self.read()[12:])
                                        message.set_src(src = self.read()[6:])
                                        message.set_data(self.read()[7:])
#                                        print message.get_message()
                                        # message.get_message() push to redis

	def read(self):
                return ser.readline()

	def write(self,message):
                        ser.writelines('<SEND>'+'\n'+str(message)+'\n')

        def set_nodeid(self,nodeid):
                ser.writelines('<SET_NODE_ID>'+'\n'+str(nodeid)+'\n')
