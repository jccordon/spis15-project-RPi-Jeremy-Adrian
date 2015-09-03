# Program to test the LEDs on Pizazz
# LED1 pin 22
# LED2 pin 18
# LED3 pin 11
# LED4 pin 07

import RPi.GPIO as GPIO, time

# Use physical pin numbering
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Define LED pins as outputs
LED1 = 22
LED2 = 18
LED3 = 11
LED4 = 07

LedOn = 0 # define On as a low
LedOff = 1

GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)

# Function to set all pins
def setLEDs(L1, L2, L3, L4):
  GPIO.output(LED1, L1)
  GPIO.output(LED2, L2)
  GPIO.output(LED3, L3)
  GPIO.output(LED4, L4)

# turn all LEDs off to start with
setLEDs(LedOff, LedOff, LedOff, LedOff)

# main loop
try:
  while True:
    setLEDs (LedOn, LedOff, LedOff, LedOff)
    time.sleep (0.2)
    setLEDs (LedOff, LedOn, LedOff, LedOff)
    time.sleep (0.2)
    setLEDs (LedOff, LedOff, LedOn, LedOff)
    time.sleep (0.2)
    setLEDs (LedOff, LedOff, LedOff, LedOn)
    time.sleep (0.2)

except KeyboardInterrupt:
  setLEDs(LedOff, LedOff, LedOff, LedOff)
  GPIO.cleanup()
