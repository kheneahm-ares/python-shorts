from configuration import *
import pygame 
import sys
from sprites import *

class Spritesheet:
    def __init__(self, path):
        self._spritesheet = pygame.image.load(path).convert()
        
    def get_image(self, x,y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self._spritesheet, (0,0), (x,y,width,height))
        
        #set transparency by replacing black with transparency
        sprite.set_colorkey(BLACK)
        return sprite
    
    
class Game:
    def __init__(self):
        self._screen = pygame.display.set_mode((MIN_WIDTH, MIN_HEIGHT))
        self._clock = pygame.time.Clock()
        self._terrain_spritesheet = Spritesheet('assets/images/terrain.png') 
        self._player_spritesheet = Spritesheet('assets/images/cats.png') 
        self._enemy_spritesheet = Spritesheet('assets/images/evil.png') 
        self._running = True
        
    def createTileMap(self):
        #row = up and down = y
        #column = left and right = x
        #this works even not on a matrix because we can enumerate a string in python
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)
                if column == 'P':
                    self.player = Player(self, j, i)
                if column == 'E':
                    Enemy(self, j, i)
    
    def create(self):
        self._all_sprites = pygame.sprite.LayeredUpdates()
        self.createTileMap()
        
    def update(self):
        self._all_sprites.update()
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

    def draw(self):
        self._screen.fill(BLACK)
        #draw the group that contains all of our sprites onto screen
        self._all_sprites.draw(self._screen)
        
        #tick and update display
        self._clock.tick(FPS)
        pygame.display.update()
    
    def main(self):
        while self._running:
            self.events()
            self.update()
            self.draw()

game = Game()
game.create()

while game._running:
    game.main()
    
pygame.quit()
sys.exit()

