from machine import Pin,PWM
from time import sleep
servoPin = PWM(Pin(16))
servoPin.freq(50)

def servo(degrees):
    if degrees>270:
        degress=270
    if degrees<0:
        degrees=0
    maxDuty=8000
    minDuty=1000
    newDuty=minDuty+(maxDuty-minDuty)*(degrees/270)
    servoPin.duty_u16(int(newDuty))
