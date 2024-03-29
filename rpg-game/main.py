from configuration import *
import pygame 
import sys
from sprites import *
from weapons import *

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
        self._weapon_spritesheet = Spritesheet('assets/images/sword.png') 
        self._bullet_spritesheet = Spritesheet('assets/images/powerBall.png') 
        self._running = True
        self.block_collided = False
        self.enemy_collided = False
        
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
                if column == 'W':
                    Water(self, j, i)
                if column == 'I':
                    Weapon(self, j, i)
    
    def create(self):
        self._all_sprites = pygame.sprite.LayeredUpdates()
        self._all_blocks = pygame.sprite.LayeredUpdates()
        self._all_enemies = pygame.sprite.LayeredUpdates()
        self._all_water = pygame.sprite.LayeredUpdates()
        self.mainPlayer  = pygame.sprite.LayeredUpdates()
        self._all_weapons = pygame.sprite.LayeredUpdates()
        self._all_bullets = pygame.sprite.LayeredUpdates()
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
    
    def camera(self):
        if self.block_collided == False and self.enemy_collided == False:
            pressed = pygame.key.get_pressed()
        
            if pressed[pygame.K_LEFT]:
                for i, sprite in enumerate(self._all_sprites):
                    sprite.rect.x += PLAYER_STEPS
            elif pressed[pygame.K_RIGHT]:
                for i, sprite in enumerate(self._all_sprites):
                    sprite.rect.x -= PLAYER_STEPS
            elif pressed[pygame.K_DOWN]:
                for i, sprite in enumerate(self._all_sprites):
                    sprite.rect.y -= PLAYER_STEPS
            elif pressed[pygame.K_UP]:
                for i, sprite in enumerate(self._all_sprites):
                    sprite.rect.y += PLAYER_STEPS
    
    def main(self):
        while self._running:
            self.events()
            self.camera()
            self.update()
            self.draw()

game = Game()
game.create()

while game._running:
    game.main()
    
pygame.quit()
sys.exit()

