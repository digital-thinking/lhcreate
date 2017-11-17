import pygame
import os
from time import sleep
import RPi.GPIO as GPIO

from StartScreen import StartScreen
config = {}
config['buttonA'] = 13
config['buttonB'] = 27
config['servo1'] = 12

#config button
GPIO.setmode(GPIO.BCM)
GPIO.setup(config['buttonA'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(config['buttonB'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(config['servo1'], GPIO.OUT)

#Colours
config['color_white'] = (255,255,255)

#config pygame
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((640, 480))
screen.fill((0,0,0))
pygame.display.update() 
config['font_big'] = pygame.font.Font(None, 100)
clock = pygame.time.Clock()        

currentScreen = StartScreen()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GPIO.cleanup()
            exit()
    currentScreen.render(config, screen)       

    
        