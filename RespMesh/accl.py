
import smbus
import time
import math

class accl():
	def init():
		print "accl init"
	def get_accl(self): 
	# Get I2C bus
		bus = smbus.SMBus(1)
		bus.write_byte_data(0x6b, 0x23, 0x30)
		bus.write_byte_data(0x6b, 0x20, 0x67)
		bus.write_byte_data(0x6b, 0x21, 0x20)
		bus.write_byte_data(0x1d, 0x24, 0x70)
		bus.write_byte_data(0x1d, 0x25, 0x60)
		bus.write_byte_data(0x1d, 0x26, 0x00)
		time.sleep(0.5)
		data0 = bus.read_byte_data(0x1d, 0x28)
		data1 = bus.read_byte_data(0x1d, 0x29)
			# Convert the data
		xAccl = data1 * 256 + data0
		if xAccl > 32767 :
			xAccl -= 65536
		data0 = bus.read_byte_data(0x1d, 0x2A)
		data1 = bus.read_byte_data(0x1d, 0x2B)

				# Convert the data
		yAccl = data1 * 256 + data0
		if yAccl > 32767 :
			yAccl -= 65536
		data0 = bus.read_byte_data(0x1d, 0x2C)
		data1 = bus.read_byte_data(0x1d, 0x2D)
	
		zAccl = data1 * 256 + data0
		if zAccl > 32767 :
			zAccl -= 65536
		
		return xAccl ,yAccl ,zAccl



