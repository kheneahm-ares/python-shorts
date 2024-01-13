from configuration import *
import pygame 
import sys

class Spritesheet:
    def __init__(self, path):
        self._spritesheet = pygame.image.load(file).convert()
        
    def game_image(self, x,y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self._spritesheet, (0,0), (x,y,width,height))

        return sprite
    
    
class Game:
    def __init__(self):
        self._screen = pygame.display.set_mode(MIN_WIDTH, MIN_HEIGHT)
        self._clock = pygame.time.Clock()
        self._terrain_spritesheet = Spritesheet('assets/images/terrain.png') #991,541
        self._running = True
        
    def createTileMap(self):
        pass
    
    def create(self):
        self._all_sprites = pygame.sprite.LayeredUpdates()
    
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