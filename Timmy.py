#Adrian J. & Jeremy C.
#Timmy (obstacle avoidance) code
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

#speed of car
speed = 100

#maximum distance
maxdist = 300

#sonar pins
front = 8
echoR = 07
triggerR = 22
echoL = 11
triggerL = 18

#takes five sonar readings, sorts from min-max, and returns its median value
def Sonar(trigger, echo): 
   dist_list=[]
   for i in range(5):
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
      dist_list = dist_list +[distance]
      time.sleep(0.01)
   sorted_list=sorted(dist_list)
   return sorted_list[2]

#functions execute cars movement
#p&q= right wheel
#a&b= left wheel
def forward(speed):
  p.ChangeDutyCycle(speed)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(speed)
  b.ChangeDutyCycle(0)
  print('forward')

def reverse(speed):
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(speed)
  a.ChangeDutyCycle(0)
  b.ChangeDutyCycle(speed)
  print('reverse')

def turnleft(speed):
  p.ChangeDutyCycle(speed)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(0)
  b.ChangeDutyCycle(speed)
  print('left')

def turnright(speed):
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(speed)
  a.ChangeDutyCycle(speed)
  b.ChangeDutyCycle(0)
  print('right')

def turnaroundright():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(20)
  time.sleep(.7)
  a.ChangeDutyCycle(20)
  time.sleep(.7)
  b.ChangeDutyCycle(0)
  stopall()
  print('turnright')

def turnaroundleft():
  p.ChangeDutyCycle(20)
  time.sleep(.6)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(0)
  b.ChangeDutyCycle(20)
  time.sleep(.6)
  stopall()
  print('turnleft')
   
def stopall():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(0)
  b.ChangeDutyCycle(0)
  print('stop')

try:
   while True:
      leftDist = Sonar(triggerL, echoL)
      frontDist = Sonar(front, front)
      rightDist = Sonar(triggerR,echoR)
      tooclose = 10
      superclose = 1000 #used when sonar touches wall and returns extremely high distances
      print 'front:', str(frontDist) + ' right:', str(rightDist) + ' left:', str(leftDist)
      fspeed = speed * (frontDist/maxdist)
      lspeed = speed * (leftDist/maxdist)
      rspeed = speed * (rightDist/maxdist)
      #prevents the car from stopping its code when sonar reading is 0
      if fspeed < 10:
         fspeed = 10
      if lspeed < 10:
         lspeed = 10
      if rspeed < 10:
         rspeed = 10
      print 'fspeed:', str(fspeed) + '  rspeed:', str(rspeed) + ' lspeed:', str(lspeed)
      #algorithm for avoiding obstacles
      if frontDist >= tooclose and rightDist >= tooclose and leftDist >= tooclose:
         forward(fspeed)
      elif frontDist >= tooclose and rightDist <= tooclose and leftDist >= tooclose:
         forward(fspeed)
         time.sleep(0.1)
         turnleft(lspeed)
      elif frontDist >= tooclose and rightDist >= tooclose and leftDist <= tooclose:
         forward(fspeed)
         time.sleep(0.1)
         turnright(rspeed)
      elif frontDist >= tooclose and rightDist <= tooclose and leftDist <= tooclose:
         reverse(20)
	 time.sleep(0.1)
	 turnaroundleft()
      elif frontDist <= tooclose or frontDist >= superclose and rightDist >= tooclose  and leftDist >= tooclose:
         reverse(20)
         time.sleep(0.1)
	 turnaroundright()
      elif frontDist <= tooclose or frontDist >= superclose and rightDist <= tooclose or rightDist >= superclose and leftDist >= tooclose:
         reverse(20)
         time.sleep(0.1)
         turnleft(lspeed)
      elif frontDist <= tooclose or frontDist >= superclose  and rightDist >= tooclose and leftDist <= tooclose or leftDist >= superclose:
         reverse(20)
         time.sleep(0.1)
         turnright(rspeed)
except KeyboardInterrupt:
   GPIO.cleanup()
