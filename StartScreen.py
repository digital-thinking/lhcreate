import pygame
import RPi.GPIO as GPIO
import os

BLOCK_BUTTON_TIME = 30
GAME_OVER_TIME = 60 * 5

class StartScreen:    
    def __init__(self):
        self.data = []
        self.image = pygame.image.load('screens/screen1.png')
        self.score = 0
        self.state = State1()
        self.buttonBlockCounter = BLOCK_BUTTON_TIME
        self.gameOverCounter = GAME_OVER_TIME
  
    def setImage(self, imagepath):
        self.image = pygame.image.load(imagepath)
    
    def reset(self):
        self.score = 0
        self.state = State1()
        self.buttonBlockCounter = BLOCK_BUTTON_TIME
        self.gameOverCounter = GAME_OVER_TIME
    
    def render(self, config, screen):        
        imagerect = self.image.get_rect()          
        
        screen.blit(self.image, imagerect)
        
        text_surface = config['font_big'].render('%d'%config['buttonA'], True, config['color_white'])            
        rect = text_surface.get_rect(center=(160,120))                   
        screen.blit(text_surface, rect)
        
        #Game over counter
        if (self.gameOverCounter == 0):
            self.state = GameOverState()            
        else:
            self.gameOverCounter -= 1
        
        #Block button counter
        if (self.buttonBlockCounter == 0):            
            if GPIO.input(config['buttonA']) == False and GPIO.input(config['buttonB']) == True:            
                self.state.onButtonA(self)
                self.buttonBlockCounter = BLOCK_BUTTON_TIME
            
            if GPIO.input(config['buttonB']) == False and GPIO.input(config['buttonA']) == True:            
                self.state.onButtonB(self)
                self.buttonBlockCounter = BLOCK_BUTTON_TIME
            
            if GPIO.input(config['buttonB']) == False and GPIO.input(config['buttonA']) == False:            
                self.state.onBothButtons(self)
                self.buttonBlockCounter = BLOCK_BUTTON_TIME
        else:
            self.buttonBlockCounter -= 1
            
            
        
        print (self.gameOverCounter)
        pygame.display.update()
        
    def setState(self, state):
        self.state = state
        
class State1:
    def onButtonA(self, screen):
        print('State1A')
        screen.setState(State2())
        screen.setImage('screens/screen2.png')         
    
    def onButtonB(self, screen):
        print('State1B')
        screen.setState(State2())
        screen.setImage('screens/screen2.png')
        
    def onBothButtons(self, screen):
        print('State1Both')

class State2:
    def onButtonA(self, screen):
        print('State2A')
        screen.setState(State1())
    
    def onButtonB(self, screen):
        print('State2B')
        screen.setState(State1())
        
    def onBothButtons(self, screen):
        print('State2Both')
        
class GameOverState:
    def onButtonA(self, screen):
        print('Game Over')        
    
    def onButtonB(self, screen):
        print('Game Over')        
        
    def onBothButtons(self, screen):
        screen.reset()
        
    
            