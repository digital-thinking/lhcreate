import RPi.GPIO as GPIO
from time import sleep

class HardwareControls:
    def __init__(self, config):
        self.config = config
        self.debugCollision = 0        
    def releaseBall(self):        
        p = GPIO.PWM(self.config['servo1'], 50)    # create an object p for PWM on port 25 at 50 Hertz  
        pwm=GPIO.PWM(12,50)
        pwm.start(3.75)
        sleep(3)

        DesiredAngle = 90
        ##DutyCycle = 1/18* (DesiredAngle) + 2
        pwm.ChangeDutyCycle(7.5)
        sleep(3)

        DesiredAngle = 180
        pwm.ChangeDutyCycle(11.25)
           
                
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