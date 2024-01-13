import pygame
from configuration import *

class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, game, x,y, layer, imageX, imageY):
        self._game = game
        
        #adding every block to groups
        self.groups = self._game._all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        #every block will start at tile position * size
        self._x = x*TILE_SIZE
        self._y = y*TILE_SIZE
        
        #inherited from sprite
        self._layer = layer
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        #create block from blitted image
        self.image = self._game._terrain_spritesheet.get_image(imageX, imageY, self.width, self.height)
        self.rect = self.image.get_rect() #set x, y coordinates of image
        self.rect.x = self._x
        self.rect.y = self._y 

class Ground(BaseSprite):
    def __init__(self, game, x,y):
        super().__init__(game, x,y, GROUND_LAYER, 447, 353)

class Block(BaseSprite):
    def __init__(self, game, x,y):
        super().__init__(game, x,y, BLOCKS_LAYER, 991, 541)