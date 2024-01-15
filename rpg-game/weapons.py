import pygame
from configuration import *
import math

class Weapon(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self._game = game
        self._layer = WEAPONS_LAYER
        self.groups = self._game._all_sprites, self._game._all_weapons
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE
        
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.animationCounter = 0
        self.image = self._game._weapon_spritesheet.get_image(447, 353, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def animation(self):
        wepAnimations = [self._game._weapon_spritesheet.get_image(0,0, self.width, self.height),
                          self._game._weapon_spritesheet.get_image(32,0, self.width, self.height),
                          self._game._weapon_spritesheet.get_image(64,0, self.width, self.height)]
        
        self.image = wepAnimations[math.floor(self.animationCounter)]
        self.animationCounter += 0.1
        if self.animationCounter >= 3:
            self.animationCounter = 0
            
    def update(self):
        self.animation()
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self.game = game
        self._layer = HEALTH_LAYER
        self.groups = self.game._all_sprites, self.game._all_bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x
        self.y = y
        
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        self.image = self.game._bullet_spritesheet.get_image(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.direction = self.game.player.direction
        
    def move(self):
        if self.direction == 'right':
            print(self.direction)
            self.rect.x += BULLET_STEPS
        if self.direction == 'left':
            print(self.direction)
            self.rect.x -= BULLET_STEPS
        if self.direction == 'up':
            print(self.direction)
            self.rect.y -= BULLET_STEPS
        if self.direction == 'down':
            self.rect.y += BULLET_STEPS
            
    def update(self):
        self.move()