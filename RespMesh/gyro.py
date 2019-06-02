import smbus
import math 
import turtle
import time
from redisConnection import RedisTools
#register




class Magn():

	def __init__(self):
		print ""
	def getNorthDegree(self):
		power_mgmt_1 = 0x6b
		power_mgmt_2 = 0x1d
		bus = smbus.SMBus(1)
		bus.write_byte_data(power_mgmt_1, 0x20, 0x67)
		bus.write_byte_data(power_mgmt_1, 0x21, 0x20)
		bus.write_byte_data(power_mgmt_2, 0x24, 0x70)
		bus.write_byte_data(power_mgmt_2, 0x25, 0x60)
		bus.write_byte_data(power_mgmt_2, 0x26, 0x00)
		mag_data_x_0 = bus.read_byte_data(power_mgmt_2, 0x08)
		mag_data_x_1 = bus.read_byte_data(power_mgmt_2, 0x09)
				# Convert the data
		xMag = mag_data_x_1 * 256 + mag_data_x_0
		if xMag > 32767 :
			xMag = xMag - 65536
		mag_data_y_0 = bus.read_byte_data(power_mgmt_2, 0x0A)
		mag_data_y_1 = bus.read_byte_data(power_mgmt_2, 0x0B)
				# Convert the data
		yMag = mag_data_y_1 * 256 + mag_data_y_0
		if yMag > 32767 :
			yMag =yMag - 65536
		mag_data_z_0 = bus.read_byte_data(power_mgmt_2, 0x0C)
		mag_data_z_1 = bus.read_byte_data(power_mgmt_2, 0x0D)
				# Convert the data
		zMag = mag_data_z_1 * 256 + mag_data_z_0
		if zMag > 32767 :
			zMag -= 65536
		
		radian =math.atan2(yMag,xMag)#*(180/ math.pi)
		haed = radian + 0.22
		if haed < 0:
			haed = haed + math.pi*2
		#if haed > math.pi*2:
		#	haed = head - 2*math.pi

		haedD = haed * (180/math.pi)
		return haedD
class commander( ):
	def __init__(self):
		print ""
	def start(self ,nodeId):
		while True:
			meX = 32.0729653
			meY = 34.8072157
			r = RedisTools()
			if r.llen(str(nodeId) + "_G") > 0 :
				data = str(r.lpop(str(nodeId) + "_G"))
				G,targetX,targetY = data.split(':',3)
			else :			
				targetX = 32.7996897
				targetY = 35.0517956
			targetX = float(targetX)
			targetY = float(targetY)
			dLon = (targetY-meY)
			y	=	math.sin(dLon)	*	math.cos(targetX)
			x	=	math.cos(meX)	*	math.sin(targetY)	-	math.sin(meX)	*	math.cos(targetY)	*	math.cos(dLon)

			brng	=	math.atan2(y,x)
			brng 	=	math.degrees(brng)
			brng	=	(brng + 360) % 360
			brng	=	360	-	brng
			magnometer = Magn()
			radians = math.atan2(targetY - meY , targetX - meX)
			degree = math.degrees(radians- 0.24) 
			degree = brng 
			mag =magnometer.getNorthDegree()
			target = (360 - mag  + degree) % 360
			degree  = "12" 
			m = 10 
			screen  = turtle.Screen()
			trtl = turtle.Turtle()

			trtl.speed(10)
			screen.setup(620,620)
			screen.bgcolor('black')
			clr = ['red','green','blue','yellow','purple']
			trtl.pensize(4)
			trtl.shape('arrow')
			trtl.pencolor('white')
	

			trtl.goto(0,0)
			trtl.left(270)
			trtl.penup()
			trtl.forward(270)
			trtl.write("Name : Haifa |"+"Distance:217.2k | "+"x:"+str(targetX)+",y:"+str(targetY),align="center",font=("Arial",12,"normal"))
			trtl.setheading(0)
			trtl.goto(0,0)
			trtl.penup()
			trtl.left(int(mag))
			trtl.forward(230)
			toprint=str("N")
			trtl.write(toprint,align="center",font=("Arial",18,"normal"))	

			trtl.setheading(0)
			trtl.goto(0,0)
			trtl.penup()
			trtl.forward(270)
			trtl.pendown()
			trtl.penup()
			trtl.write(str(degree),align="center",font=("Arial",22,"normal"))

			trtl.setheading(0)
			trtl.goto(0,0)
			trtl.left(int(target))
			trtl.pendown()
			trtl.forward(150)
			trtl.penup()
			toprint=str((int(target)))
			trtl.write(toprint,align="center",font=("Arial",18,"normal"))
	

			time.sleep(2)
			trtl.ht()
			trtl.clear()





