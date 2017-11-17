import pygame
import os
from HardwareControls import HardwareControls

BLOCK_BUTTON_TIME = 10
GAME_OVER_TIME = 60 * 5
DELAY = 10

class StartScreen:    
    def __init__(self, config):        
        self.data = []
        self.hardwareControls = HardwareControls(config)
        self.config = config
        self.collisions = [False, False, False, False]
        self.state = State1()
        self.buttonBlockCounter = BLOCK_BUTTON_TIME
        self.gameOverCounter = GAME_OVER_TIME
        
    def reset(self):
        self.collisions = [False, False, False, False]
        self.state = State1()
        self.buttonBlockCounter = BLOCK_BUTTON_TIME
        self.gameOverCounter = GAME_OVER_TIME
    
    def render(self, screen):        
        imagerect = self.state.getImage().get_rect()       
        screen.blit(self.state.getImage(), imagerect)   
        
        #Game over counter
        if (self.gameOverCounter == 0):
            self.state = GameOverState()            
        else:
            self.gameOverCounter -= 1
        
        #Block button counter
        if (self.buttonBlockCounter == 0):            
            if self.hardwareControls.isOnlyButtonA():
                self.state.onButtonA(self)
                self.buttonBlockCounter = BLOCK_BUTTON_TIME
            
            if self.hardwareControls.isOnlyButtonB():
                self.state.onButtonB(self)
                self.buttonBlockCounter = BLOCK_BUTTON_TIME
            
            if self.hardwareControls.isBothButtons():          
                self.state.onBothButtons(self)
                self.buttonBlockCounter = BLOCK_BUTTON_TIME
        else:
            self.buttonBlockCounter -= 1
       
        if (self.hardwareControls.getCollision() > 0):
            self.state.handleCollision(self, self.hardwareControls.getCollision())
            
        self.state.act(self)        
        if (self.collisions[0] and self.collisions[1] and self.collisions[2] and self.collisions[3]):
            print ('game success')
            self.state = WinState()

        progressBar = pygame.Surface((1280 * self.gameOverCounter / GAME_OVER_TIME, 100))      
        progressBar.fill((200,0,0))
        screen.blit(progressBar ,pygame.Rect(0,0,0,0))        

        pygame.display.update()
        
    def setState(self, state):
        print (state)
        self.state = state

class NothingState():
    def onButtonA(self, screen):      
        print('A - Do nothing')
    
    def onButtonB(self, screen):       
        print('B - Do nothing')
        
    def onBothButtons(self, screen):
        print('Both - Do nothing')
       
    def getImage(self):
        return pygame.image.load('screens/screen1.png')
    
    def handleCollision(self, screen, number):
        print('Collision - Do nothing')
        
    def act(self, screen):
        pass
        

class State1(NothingState):        
    def onBothButtons(self, screen):
        print('Start Game')        
        screen.setState(State2())
        screen.hardwareControls.releaseBall()
        
class DelayedState(NothingState):
    def __init__(self, steps, nextState):
        self.counter = steps
        self.nextState = nextState
        
    def act(self, screen):
        self.counter -= 1
        if (self.counter == 0):
            screen.setState(self.nextState)
        pass
        

class State2(NothingState):    
    def getImage(self):
        return pygame.image.load('screens/screen2.png')
    
    def handleCollision(self, screen, number):
        screen.collisions[number-1] = True
        screen.setState(DelayedState(DELAY, State1()))
        print('Collided: ' + str(number))
        
class GameOverState(NothingState):
    def onButtonA(self, screen):
        print('Game Over')        
    
    def onButtonB(self, screen):
        print('Game Over')        
        
    def onBothButtons(self, screen):
        screen.reset()
        
    def getImage(self):
        return pygame.image.load('screens/screen_go.png')
    
        
class WinState(NothingState):
    def onButtonA(self, screen):
        print('Game Over')        
    
    def onButtonB(self, screen):
        print('Game Over')        
        
    def onBothButtons(self, screen):
        screen.reset()
        
    def getImage(self):
        return pygame.image.load('screens/screen_win.png')     
            