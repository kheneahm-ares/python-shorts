import pygame
from configuration import *
import random
import math

class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, game, x,y, layer, image):
        self._game = game
        
        #adding every block to groups
        self._layer = layer
        self.groups = self._game._all_sprites
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        #every block will start at tile position * size
        self._x = x*TILE_SIZE
        self._y = y*TILE_SIZE
        
        #inherited from sprite
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        #create block from blitted image
        self.image = image
        self.rect = self.image.get_rect() #set x, y coordinates of image
        self.rect.x = self._x
        self.rect.y = self._y 

class Ground(BaseSprite):
    def __init__(self, game, x,y):
        super().__init__(game, x,y, GROUND_LAYER, game._terrain_spritesheet.get_image(447, 353, TILE_SIZE, TILE_SIZE))

class Block(BaseSprite):
    def __init__(self, game, x,y):
        super().__init__(game, x,y, BLOCKS_LAYER, game._terrain_spritesheet.get_image(991, 541, TILE_SIZE, TILE_SIZE))
        
class Player(BaseSprite):
    def __init__(self, game, x,y):
        self.x_change = 0
        self.y_change = 0
        self.direction = "down"
        self.animationCounter = 0
        super().__init__(game, x,y, PLAYER_LAYER, game._player_spritesheet.get_image(0, 0, TILE_SIZE, TILE_SIZE))
    
    def move(self):
        key_pressed = pygame.key.get_pressed()
        
        if key_pressed[pygame.K_LEFT]:            
            self.x_change -= PLAYER_STEPS
            self.direction = "left"
        elif key_pressed[pygame.K_RIGHT]:
            self.x_change += PLAYER_STEPS
            self.direction = "right"
        elif key_pressed[pygame.K_DOWN]:
            self.y_change += PLAYER_STEPS
            self.direction = "down"
        elif key_pressed[pygame.K_UP]:
            self.y_change -= PLAYER_STEPS
            self.direction = "up"

    def update(self):
        self.move()
        self.animation()
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change
        
        #reset the            
        self.x_change = 0
        self.y_change = 0
        
    def animation(self):
        downAnimations = [self._game._player_spritesheet.get_image(0,0, self.width, self.height),
                          self._game._player_spritesheet.get_image(32,0, self.width, self.height),
                          self._game._player_spritesheet.get_image(64,0, self.width, self.height)]
        upAnimations = [self._game._player_spritesheet.get_image(0,96, self.width, self.height),
                          self._game._player_spritesheet.get_image(32,96, self.width, self.height),
                          self._game._player_spritesheet.get_image(64,96, self.width, self.height)]
        leftAnimations = [self._game._player_spritesheet.get_image(0,32, self.width, self.height),
                          self._game._player_spritesheet.get_image(32,32, self.width, self.height),
                          self._game._player_spritesheet.get_image(64,32, self.width, self.height)]
        rightAnimations = [self._game._player_spritesheet.get_image(0,64, self.width, self.height),
                          self._game._player_spritesheet.get_image(32,64, self.width, self.height),
                          self._game._player_spritesheet.get_image(64,64, self.width, self.height)]
        
        if self.direction == 'down':
            self.animate(downAnimations)
        if self.direction == 'up':
            self.animate(upAnimations)

        if self.direction == 'left':
            self.animate(leftAnimations)
        
        if self.direction == 'right':
            self.animate(rightAnimations)

    def animate(self, lstAnimation):
            if self.y_change  == 0 and self.x_change == 0:
                self.image = lstAnimation[0]
            else:
                self.image = lstAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter = 1 #not 0 bc that's standing still 
class Enemy(BaseSprite):
    def __init__(self, game, x,y):
        self.x_change = 0
        self.y_change = 0
        self.direction = random.choice(['left','right', 'up', 'down'])
        self.maxSteps = random.choice([80, 100, 120])
        self.maxStall = 40
        self.currentSteps = 0
        self.state = 'moving'
        
        super().__init__(game, x,y, ENEMY_LAYER, game._enemy_spritesheet.get_image(0, 0, TILE_SIZE, TILE_SIZE))
        
    def move(self):
        if self.state == 'moving':
            
            if self.direction == "left":            
                self.x_change -= ENEMY_STEPS
                
            elif self.direction == "right":
                self.x_change += ENEMY_STEPS
                
            elif self.direction == "down":
                self.y_change += ENEMY_STEPS
                
            elif self.direction == "up":
                self.y_change -= ENEMY_STEPS
            
            self.currentSteps += 1
            
        elif self.state == "stalling":
            self.currentSteps += 1
            if self.currentSteps == self.maxStall:
                self.state = 'moving'
                self.currentSteps = 0
    
    def update(self):
        self.move()
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change
        
        #reset the            
        self.x_change = 0
        self.y_change = 0
        
        if self.currentSteps == self.maxSteps:
            if self.state != 'stalling':
                self.currentSteps = 0
                
            self.direction = random.choice(['left','right', 'up', 'down'])
            self.maxSteps = random.choice([80, 100, 120])
            self.state = "stalling"
