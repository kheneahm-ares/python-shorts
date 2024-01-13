import pygame
from configuration import *

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self._game = game
        
        #adding every block to groups
        self.groups = self.game._all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        #every block will start at tile position * size
        self._x = x*TILE_SIZE
        self._y = y*TILE_SIZE
        
        #inherited from sprite
        self._layer = GROUND_LAYER
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        #create block from blitted image
        self.image = self.game._terrain_spritesheet.get_spirte(447, 353, self.width, self.height)
        self.rect = self.image.get_rect() #set x, y coordinates of image
        self.rect.x = self._x
        self.rect.y = self._y

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self._game = game
        
        #adding every block to groups
        self.groups = self.game._all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        #every block will start at tile position * size
        self._x = x*TILE_SIZE
        self._y = y*TILE_SIZE
        
        #inherited from sprite
        self._layer = BLOCKS_LAYER
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        #create block from blitted image
        self.image = self.game._terrain_spritesheet.get_spirte(991, 541, self.width, self.height)
        self.rect = self.image.get_rect() #set x, y coordinates of image
        self.rect.x = self._x
        self.rect.y = self._y