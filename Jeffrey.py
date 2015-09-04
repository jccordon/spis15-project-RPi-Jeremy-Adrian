import RPi.GPIO as GPIO, sys, threading, time

#use physical pin numbering
GPIO.setmode(GPIO.BOARD)

#use pwm on inputs so motors don't go too fast
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

# Define Sonar Pin for Trigger and Echo to be the same
left = 8
triggerR = 18
echoR = 12

#mspeed
speed = 100

def Sonar(trigger, echo):
    dist_list = []
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
       # multiplied by the mspeed of sound (cm/s)
       distance = elapsed * 34000
       # That was the distance there and back so halve the value
       distance = distance / 2
       time.sleep(0.01)
       sorted_list = sorted(dist_list)
       return sorted_list[2]

def forward(speed):
  p.ChangeDutyCycle(speed)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle()
  b.ChangeDutyCycle(0)
  print('straight')

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

def stopall():
  p.ChangeDutyCycle(0)
  q.ChangeDutyCycle(0)
  a.ChangeDutyCycle(0)
  b.ChangeDutyCycle(0)
  print('stop')

def friend():
    try:
        while True:
            lDist = Sonar(left,left)
            rDist = Sonar(triggerR,echoR)
            tooclose = 10
            close = range(10,30)
            far = 30
            print 'lDist:', lDist + ' rDist:', rDist
            lspeed = speed * (lDist,maxdist)
            rspeed = speed * (rDist,maxdist)
            if lDist >= far and rDist >= far:
                stopall()
            if lDist <= tooclose and rDist <= tooclose:
                stopall()
            elif lDist in close and rDist in close:
                forward(10)
            elif lDist in close and rDist >= far:
                forward(10)
                time.sleep(0.1)
                turnleft(lspeed)
            elif lDist >= far and rDist in close:
                forward(10)
                time.sleep(0.1)
                turnright(rspeed)
            
                
