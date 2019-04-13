import os,subprocess,signal
import serial
from rfbridge import RFBridge 
import threading
import time
import platform
from Message import Message
from redisConnection import RedisTools
from config import Config
import zipfile

conf = Config()
redisTool = RedisTools()
bridge = RFBridge(conf.node_id,redisTool)

#proc = subprocess.Popen(['bash','./recorder.sh'])
#time.sleep(3)

#proc.kill()
#proc = subprocess.Popen(['sudo','./usbreset','/dev/bus/usb/001/011'])
#time.sleep(2)
#proc.send_signal(signal.SIGKILL)


#ziped = zipfile.ZipFile('./media/test.zip','w');
#ziped.write('./media/test.mp3', compress_type=zipfile.ZIP_DEFLATED);
#ziped.close()


COM = '/dev/ttyUSB0'
ser = serial.Serial(COM,115200)


t = threading.Thread(name = 'just',target=bridge.begin)
t.start()

with open('./media/test.tar.gz','rb') as f:
	print "Running..."
	ser.writelines('<AUDIO>\n')
	time.sleep(1);
	byte = f.read(100)
	ser.writelines(byte)
	while byte != "":
		byte = f.read(100)
		ser.writelines(byte)
		time.sleep(0.1)




#wav = './media/test.wav'
#cmd = 'lame --preset insane %s' % wav
#subprocess.call(cmd,shell=True)
