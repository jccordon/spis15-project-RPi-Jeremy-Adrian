#Afrian J. & Jeremy C.
#Timmy (follower) code
#Combine sonar detection with movement

import RPi.GPIO as GPIO, sys, threading, time

#removes the annoying warnings 
GPIO.setwarnings(False)

#use physical pin numbering
GPIO.setmode(GPIO.BOARD)

#use pwm on inputs so motors don't go too fast
# Pins 19, 21 Right Motor
# Pins 24, 26 Left Motor
GPIO.setup(19, GPIO.OUT)
p=GPIO.PWM(19, 20)
p.start(0)
GPIO.setup(21, GPIO.OUT)
q=GPIO.PWM(21, 20)
q.start(0)
GPIO.setup(24, GPIO.OUT)
a=GPIO.PWM(24,20)
a.start(0)
GPIO.setup(26, GPIO.OUT)
b=GPIO.PWM(26,20)
b.start(0)

#Motor Speed
slowspeed = 10
midspeed = 25
fastspeed = 50

#Sonar Pins
front = 8
echoR = 07
triggerR = 22
echoL = 11
triggerL = 18

def FrontSonar():
   try:
      while True:
         GPIO.setup(front, GPIO.OUT)
         GPIO.output(front, True)
         time.sleep(0.00001)
         GPIO.output(front, False)
         start = time.time()
         count = time.time()
         GPIO.setup(front, GPIO.IN)
         while GPIO.input(front)==0 and time.time()-count<0.1:
            start = time.time()
         stop=time.time()
         while GPIO.input(front)==1:
            stop = time.time()
         # Calculate pulse length
         elapsed = stop-start
         # Distance pulse travelled in that time is time
         # multiplied by the speed of sound (cm/s)
         distance = elapsed * 34000
         # That was the distance there and back so halve the value
         distance = distance / 2
         print 'Distance = ' + str(distance)
         return distance
         #time.sleep(1)
         
   except KeyboardInterrupt:
         GPIO.cleanup()
         
def SideSonar(trigger, echo):
   try:
      while True:
         GPIO.setup(trigger, GPIO.OUT)
         GPIO.output(trigger, True)
         time.sleep(0.00001)
         GPIO.output(trigger, False)
         start = time.time()
         count = time.time()
         GPIO.setup(echo, GPIO.IN)
         while GPIO.input(echo)==0 and time.time()-count<0.1:
            start = time.time()
         stop=time.time()
         while GPIO.input(echo)==1:
            stop = time.time()
         # Calculate pulse length
         elapsed = stop-start
         # Distance pulse travelled in that time is time
         # multiplied by the speed of sound (cm/s)
         distance = elapsed * 34000
         # That was the distance there and back so halve the value
         distance = distance / 2
         return 'Distance:', distance
         time.sleep(1)

   except KeyboardInterrupt:
      GPIO.cleanup()

def forwards():
  p.ChangeDutyCycle(slowspeed)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(slowspeed)
  b.ChangeDutyCycle(0)
  print('straight')

def reverse():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(slowspeed)
  a.ChangeDutyCycle(0)
  b.ChangeDutyCycle(fastspeed)
  print('backwards')

def turnleft():
#p & q= right wheel
#a & b= left wheel
  p.ChangeDutyCycle(fastspeed)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(slowspeed)
  b.ChangeDutyCycle(0)
  print('left')

def turnright():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(midspeed)
  a.ChangeDutyCycle(midspeed)
  b.ChangeDutyCycle(0)
  print('right')

def stopall():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(0)
  b.ChangeDutyCycle(0)
  print('stop')

def forward():
   forwards()
   time.sleep(1)

def follow():
   sonardistance = FrontSonar()
   forwards()
   time.sleep(.001)
   if sonardistance <= 5:
      return stopall()
   else:
      return follow()
      
