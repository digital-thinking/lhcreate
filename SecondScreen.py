from StartScreen import StartScreenimport 
class SecondScreen():
    
    def __init__(self):
        self.data = []
        self.image = pygame.image.load('screens/screen2.png')
        
    def render(self, config, screen):
        print('render')