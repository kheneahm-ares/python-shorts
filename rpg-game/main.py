from configuration import *
import pygame 
import sys

class Game:
    def __init__(self):
        self._screen = pygame.display.set_mode(MIN_WIDTH, MIN_HEIGHT)
        self._clock = pygame.time.Clock()
        self._running = True
        
    def createTileMap(self):
        pass
    
    def create(self):
        pass
    
    def update():
        pass
    
    def events():
        pass

    def draw():
        pass
    
    def main():
        pass

game = Game()
game.create()

while game.running:
    game.main()
    
pygame.quit()
sys.exit()