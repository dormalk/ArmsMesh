import smbus
import math 

#register
power_mgmt_1	=	0x6b
power_mgmt_2	=	0x6c

def	read_byte(reg):
	return bus.read_byte_data(address,reg)

def	read_word(reg):
	h 	=	read_byte(reg)
	l	=	read_byte(reg+1)
	value	=	(h	<<	8)	+	l
	return vaule

def read_word_2_c(reg):
	val 	=	read_word(reg)
	if(val	>=	0x8000):
		return	-((65535	-	val)	+1)
	else:
		return	val

def dist(a,b):
	return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y.z):
	radians	=	math.atan2(x,dist(y,z))
	return -math.degrees(radians)

def get_x_rotation(x,y,z):
	radians	=	math.atan2(x,dist(x,z))
	return -math.degrees(radians)

bus	
