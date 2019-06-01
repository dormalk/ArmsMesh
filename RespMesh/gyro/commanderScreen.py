import turtle
import time
import math
import gyro
from redisConnection import RedisTools
def commander(self ,nodeId):
	meX = 32.0729653
	meY = 34.8072157
	r = RedisTools()
	data = r.lpop(nodeId + "_G")
	G,targetX,targetY = data.split(':')	
#targetX = 32.7996897
#targetY = 35.0517956
	

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
		
	print "d : %f "%degree 
	print "m : %f "%mag
	print "r : %f "%radians
	print "t : %f "%target
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


