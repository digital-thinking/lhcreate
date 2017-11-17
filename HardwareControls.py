import RPi.GPIO as GPIO
from time import sleep
from random import randint

class HardwareControls:
    def __init__(self, config):
        self.config = config
        self.debugCollision = 0        
    def releaseBall(self):        
        pwm = GPIO.PWM(self.config['servo1'], 50)
        pwm.start(3.75)
        sleep(3)

        desiredAngle = 90
        dutyCycle = desiredAngle/24 + 3.75
        pwm.ChangeDutyCycle(dutyCycle)
        sleep(3)

        desiredAngle = 180
        dutyCycle = desiredAngle/24 + 3.75
        pwm.ChangeDutyCycle(dutyCycle)
           
                
    def isOnlyButtonA(self):
        return GPIO.input(self.config['buttonA']) == False and GPIO.input(self.config['buttonB']) == True

    def isOnlyButtonB(self):
        return GPIO.input(self.config['buttonB']) == False and GPIO.input(self.config['buttonA']) == True
            
    def isBothButtons(self):
        return GPIO.input(self.config['buttonB']) == False and GPIO.input(self.config['buttonA']) == False
    
    def getCollision(self):
        if (GPIO.input(self.config['collisionA']) == False):
            return 1
        if (GPIO.input(self.config['collisionB']) == False):
            return 2        
        if (GPIO.input(self.config['collisionC']) == False):
            return 3
        if (GPIO.input(self.config['collisionD']) == False):
            return 4
        
        return 0