import os,subprocess,signal
import threading
import time
import serial


#proc = subprocess.Popen(['bash','./recorder.sh'])
#time.sleep(3)

#proc.kill()
#proc = subprocess.Popen(['sudo','./usbreset','/dev/bus/usb/001/011'])
#time.sleep(2)
#proc.send_signal(signal.SIGKILL)

COM = '/dev/ttyUSB0'
ser = serial.Serial(COM,115200)

with open('./media/test.wav','rb') as f:
	ser.writelines('<AUDIO>\n')
	byte = f.read(22)
	ser.writelines(byte)
	while byte != "":
		if (ser.in_waiting > 0):
			print ser.readline()
		ser.writelines('<AUDIO>\n')
		byte = f.read(22)
		ser.writelines(byte)





