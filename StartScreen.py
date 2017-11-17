import pygame
import os
from HardwareControls import HardwareControls
from random import shuffle

BLOCK_BUTTON_TIME = 10
GAME_OVER_TIME = 60 * 10
DELAY = 10

class StartScreen:    
    def __init__(self, config):        
        self.data = []
        self.images = [pygame.image.load('screens/screen1.png'),pygame.image.load('screens/screen2.png'), pygame.image.load('screens/screen3.png'),pygame.image.load('screens/screen4.png')  ]       
        self.hardwareControls = HardwareControls(config)
        self.config = config
        self.collisions = [False, False, False, False] 
        self.state = State1()
        self.buttonBlockCounter = BLOCK_BUTTON_TIME
        self.gameOverCounter = GAME_OVER_TIME
        self.win = False
    
    def winTheGame(self):
        self.win = True
        
    def getCurrentExperiment(self):
        solved = int(self.collisions[0]) + int(self.collisions[1]) +int(self.collisions[2]) +int(self.collisions[3])
        print('Solved ' + str(solved))
        return self.images[solved]
   
   
    def reset(self):        
        self.collisions = [False, False, False, False]
        self.win = False
        self.state = State1()
        self.buttonBlockCounter = BLOCK_BUTTON_TIME
        self.gameOverCounter = GAME_OVER_TIME
    
    def render(self, screen):        

        
        #Game over counter
        if (self.gameOverCounter == 0):
            self.state = GameOverState()            
        else:
            if (self.state.isCounting()):
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
        if (self.collisions[0] and self.collisions[1] and self.collisions[2] and self.collisions[3] and not self.win):
            print ('collision success')
            self.state = State3()

        imagerect = self.state.getImage(self).get_rect()       
        screen.blit(self.state.getImage(self), imagerect)   

        progressBar = pygame.Surface((1280 * self.gameOverCounter / GAME_OVER_TIME, 20))      
        progressBar.fill((0,0,0))
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
       
    def getImage(self, screen):
        return pygame.image.load('screens/screen_start.png')
    
    def handleCollision(self, screen, number):
        #print('Collision - Do nothing')
        pass
        
    def act(self, screen):
        pass
    
    def isCounting(self):
        return False

class DelayedState(NothingState):
    def __init__(self, steps, nextState):
        self.counter = steps
        self.nextState = nextState
        
    def act(self, screen):
        self.counter -= 1
        if (self.counter == 0):
            screen.setState(self.nextState)
            
class State1(NothingState):        
    def onBothButtons(self, screen):
        print('Start Game')        
        screen.setState(State2())
        screen.hardwareControls.releaseBall()       
    
    def getImage(self, screen):
        return pygame.image.load('screens/screen_start.png')  
        

    
class State2(NothingState):        
    def handleCollision(self, screen, number):
        if (screen.collisions[number-1] == True):
            return
        screen.setState(StateQuestion(number-1))        
        print('Collided: ' + str(number))
        
    def isCounting(self):
        return True  
 
    def getImage(self, screen):
        return pygame.image.load('screens/screen_hurry.png')    

class StateQuestion(NothingState):
    def __init__(self, num):
        self.num = num
    
    def getImage(self, screen):
        return screen.getCurrentExperiment()
    
    def onButtonA(self, screen):      
        screen.setState(DelayedState(DELAY, State1()))
        screen.collisions[self.num] = True 
        
    def onButtonB(self, screen):      
        screen.setState(DelayedState(DELAY, State1()))
        screen.collisions[self.num] = True        
        
class State3(NothingState):    
    def onButtonA(self, screen):      
        screen.setState(WinState())
        screen.winTheGame()
        
    def onButtonB(self, screen):      
        screen.setState(WinState())
        screen.winTheGame()
        
    def isCounting(self):
        return True
    
    def getImage(self, screen):
        return pygame.image.load('screens/alternative.png')
    
class GameOverState(NothingState):
    def onButtonA(self, screen):
        print('Game Over')        
    
    def onButtonB(self, screen):
        print('Game Over')        
        
    def onBothButtons(self, screen):
        screen.reset()
        
    def getImage(self, screen):
        return pygame.image.load('screens/screen_go.png')
    
        
class WinState(NothingState):
    def onButtonA(self, screen):        
        print('Game Over')        
    
    def onButtonB(self, screen):
        print('Game Over')        
        
    def onBothButtons(self, screen):
        screen.reset()
        
    def getImage(self, screen):
        return pygame.image.load('screens/ENDSLIDE.png')     
            