from configuration import *
import pygame 
import sys
from sprites import *

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
        #row = up and down = y
        #column = left and right = x
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)
    
    def create(self):
        self._all_sprites = pygame.sprite.LayeredUpdates()
        self.createTileMap()
        
    def update(self):
        self._all_sprites.update()
    
    def events():
        pass

    def draw(self):
        self.screen.fill(BLACK)
        #draw the group that contains all of our sprites onto screen
        self._all_sprites.draw(self._screen)
        
        #tick and update display
        self.clock.tick(FPS)
        pygame.display.update()
    
    def main():
        pass

game = Game()
game.create()

while game.running:
    game.main()
    
pygame.quit()
sys.exit()