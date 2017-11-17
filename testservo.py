import pygame
import os
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

while True:
    for x in range(0, 150):
        GPIO.output(12, 1)
        sleep(2.5)
        GPIO.output(12, 0)
        sleep(17.5)
        
    for x in range(0, 150):
        GPIO.output(12, 1)
        sleep(0.75)
        GPIO.output(12, 0)
        sleep(19.25)

##p = GPIO.PWM(12, 50)    # create an object p for PWM on port 25 at 50 Hertz
##p.start(10.5)
##p.ChangeDutyCycle(0.075)
##sleep(1)

##p.stop()              
GPIO.cleanup()