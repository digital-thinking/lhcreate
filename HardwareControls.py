import RPi.GPIO as GPIO

class HardwareControls:
    def __init__(self, config):
        self.config = config
        self.debugCollision = 0        
    def releaseBall(self):        
        p = GPIO.PWM(self.config['servo1'], 50)    # create an object p for PWM on port 25 at 50 Hertz  
        p.start(50)             # start the PWM on 50 percent duty cycle  
                                # duty cycle value can be 0.0 to 100.0%, floats are OK  
          
        p.ChangeDutyCycle(50)   # change the duty cycle to 90%  
          
        p.ChangeFrequency(100)  # change the frequency to 100 Hz (floats also work)  
                                # e.g. 100.5, 5.2  
          
        p.stop()              
                
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