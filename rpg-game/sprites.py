import pygame
from configuration import *
import random
import math
from weapons import *

class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, game, x,y, layer, image, groups):
        self._game = game
        
        #adding every block to groups
        self._layer = layer
        self.groups = groups
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
        super().__init__(game, x,y, GROUND_LAYER, game._terrain_spritesheet.get_image(447, 353, TILE_SIZE, TILE_SIZE), (game._all_sprites))

class Water(BaseSprite):
    def __init__(self, game, x,y):
        self.animationCounter = 0
        super().__init__(game, x,y, GROUND_LAYER, game._terrain_spritesheet.get_image(865, 160, TILE_SIZE, TILE_SIZE), (game._all_sprites, game._all_blocks))

    def animation(self):
        water = [self._game._terrain_spritesheet.get_image(864,160, self.width, self.height),
                          self._game._terrain_spritesheet.get_image(896,160, self.width, self.height),
                          self._game._terrain_spritesheet.get_image(928,160, self.width, self.height)]
        self.image = water[math.floor(self.animationCounter)]
        self.animationCounter += 0.1
        if self.animationCounter >= 3:
            self.animationCounter = 0
    
    def update(self):
        self.animation()
            


class Block(BaseSprite):
    def __init__(self, game, x,y):
        super().__init__(game, x,y, BLOCKS_LAYER, game._terrain_spritesheet.get_image(991, 541, TILE_SIZE, TILE_SIZE),  (game._all_sprites, game._all_blocks))
        
class Player(BaseSprite):
    def __init__(self, game, x,y):
        self.x_change = 0
        self.y_change = 0
        self.direction = "down"
        self.animationCounter = 0
        self.healthbar = Player_HealthBar(game, x, y)
        self.swordEquipped = False
        self.waitTime = 10
        self.waitCounter = 0
        self.shootState = "shoot"
        self.currentHealth = PLAYER_MAX_HEALTH
        self.totalHealth = PLAYER_MAX_HEALTH
        super().__init__(game, x,y, PLAYER_LAYER, game._player_spritesheet.get_image(0, 0, TILE_SIZE, TILE_SIZE), (game._all_sprites, game.mainPlayer))
    
    def takeDamage(self, amount):
        self.currentHealth -= amount
        self.healthbar.damage(self.currentHealth, self.totalHealth)
        
        if self.currentHealth <= 0:
            self.kill()
            self.healthbar.kill()
            
    def waitAfterShoot(self):
        if self.shootState == 'wait':
            self.waitCounter += 1
            if self.waitCounter >= self.waitTime:
                self.shootState = 'shoot'
                self.waitCounter = 0
    
    def shoot_sword(self):
        pressed = pygame.key.get_pressed()
        if self.shootState == 'shoot':
            if self.swordEquipped:
                if pressed[pygame.K_z]:
                    Bullet(self._game, self.rect.x, self.rect.y)
                    self.shootState = 'wait'
    
    def move(self):
        key_pressed = pygame.key.get_pressed()
            
        if key_pressed[pygame.K_LEFT]:
            self.particle = Particle(self._game, self._x, self._y)                        
            self.x_change -= PLAYER_STEPS
            self.direction = "left"
        elif key_pressed[pygame.K_RIGHT]:
            self.particle = Particle(self._game, self._x, self._y)                        
            self.x_change += PLAYER_STEPS
            self.direction = "right"
        elif key_pressed[pygame.K_DOWN]:
            self.particle = Particle(self._game, self._x, self._y)                        
            self.y_change += PLAYER_STEPS
            self.direction = "down"
        elif key_pressed[pygame.K_UP]:
            self.particle = Particle(self._game, self._x, self._y)                        
            self.y_change -= PLAYER_STEPS
            self.direction = "up"

    def update(self):
        self.move()
        self.animation()
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change
        
        self.collide_block()
        self.collide_enemy()
        self.collide_weapon()
        self.shoot_sword()
        self.waitAfterShoot()
        
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
                    
    def collide_block(self):
        #negating steps moved
        pressed = pygame.key.get_pressed()
        collide = pygame.sprite.spritecollide(self, self._game._all_blocks, False, pygame.sprite.collide_rect_ratio(0.9))
        collideWater = pygame.sprite.spritecollide(self, self._game._all_water, False, pygame.sprite.collide_rect_ratio(0.9))
        
        if collide or collideWater:
            self._game.block_collided = True
            if pressed[pygame.K_LEFT]:
                self.rect.x += PLAYER_STEPS
            elif pressed[pygame.K_RIGHT]:
                self.rect.x -= PLAYER_STEPS
            elif pressed[pygame.K_UP]:
                self.rect.y += PLAYER_STEPS
            elif pressed[pygame.K_DOWN]:
                self.rect.y -= PLAYER_STEPS
        else:
            self._game.block_collided = False
            
            
        
    def collide_enemy(self):
        #negating steps moved
        pressed = pygame.key.get_pressed()
        collide = pygame.sprite.spritecollide(self, self._game._all_enemies, False, pygame.sprite.collide_rect_ratio(0.9))
        
        if collide:
            self._game.enemy_collided = True
            
            if pressed[pygame.K_LEFT]:
                self.rect.x += PLAYER_STEPS
            elif pressed[pygame.K_RIGHT]:
                self.rect.x -= PLAYER_STEPS
            elif pressed[pygame.K_UP]:
                self.rect.y += PLAYER_STEPS
            elif pressed[pygame.K_DOWN]:
                self.rect.y -= PLAYER_STEPS
        else:
            self._game.enemy_collided = False
    def collide_weapon(self):
        #negating steps moved
        collide = pygame.sprite.spritecollide(self, self._game._all_weapons, True, pygame.sprite.collide_rect_ratio(0.9))
        if collide:
            self.swordEquipped = True
            
class Enemy(BaseSprite):
    def __init__(self, game, x,y):
        self.x_change = 0
        self.y_change = 0
        self.direction = random.choice(['left','right', 'up', 'down'])
        self.maxSteps = random.choice([80, 100, 120])
        self.maxStall = 40
        self.currentSteps = 0
        self.state = 'moving'
        self.animationCounter = 0
        self.healthbar = Enemy_HealthBar(game, self, x, y)
        self.currentHealth = ENEMY_MAX_HEALTH
        self.totalHealth = ENEMY_MAX_HEALTH
        self.shootCounter = 0
        self.waitShoot = random.choice([10,20,30,40,50])
        self.shootState = 'wait'
        
        super().__init__(game, x,y, ENEMY_LAYER, game._enemy_spritesheet.get_image(0, 0, TILE_SIZE, TILE_SIZE), (game._all_sprites, game._all_enemies))
    
    def shoot(self):
        self.shootCounter += 1
            
        if self.shootCounter == self.waitShoot:
            self.shootState = 'shoot'
            self.shootCounter = 0
            self.waitShoot = random.choice([10,20,30,40,50])
            
        if self.shootState == 'shoot':
            Enemy_Bullet(self._game, self.rect.x, self.rect.y)
            self.shootState = 'wait'
                    
    def takeDamage(self, amount):
        self.currentHealth -= amount
        self.healthbar.damage(self.currentHealth, self.totalHealth)
        
        if self.currentHealth <= 0:
            self.kill()
            self.healthbar.kill()
            
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
                self.direction = random.choice(['left','right', 'up', 'down'])
                
    
    def update(self):
        self.move()
        self.animation()
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change
        
        #reset the            
        self.x_change = 0
        self.y_change = 0
        
        if self.currentSteps == self.maxSteps:
            if self.state != 'stalling':
                self.currentSteps = 0
                
            self.maxSteps = random.choice([80, 100, 120])
            self.state = "stalling"
        
        self.collide_block()
        self.collide_player()
        self.shoot()
    def animation(self):
        downAnimations = [self._game._enemy_spritesheet.get_image(0,0, self.width, self.height),
                          self._game._enemy_spritesheet.get_image(32,0, self.width, self.height),
                          self._game._enemy_spritesheet.get_image(64,0, self.width, self.height)]
        upAnimations = [self._game._enemy_spritesheet.get_image(0,96, self.width, self.height),
                          self._game._enemy_spritesheet.get_image(32,96, self.width, self.height),
                          self._game._enemy_spritesheet.get_image(64,96, self.width, self.height)]
        leftAnimations = [self._game._enemy_spritesheet.get_image(0,32, self.width, self.height),
                          self._game._enemy_spritesheet.get_image(32,32, self.width, self.height),
                          self._game._enemy_spritesheet.get_image(64,32, self.width, self.height)]
        rightAnimations = [self._game._enemy_spritesheet.get_image(0,64, self.width, self.height),
                          self._game._enemy_spritesheet.get_image(32,64, self.width, self.height),
                          self._game._enemy_spritesheet.get_image(64,64, self.width, self.height)]
        
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

    def collide_block(self):
        #negating steps moved
        collide = pygame.sprite.spritecollide(self, self._game._all_blocks, False, pygame.sprite.collide_rect_ratio(0.9))
        collideWater = pygame.sprite.spritecollide(self, self._game._all_water, False, pygame.sprite.collide_rect_ratio(0.9))
        
        if collide or collideWater:
            if self.direction == 'left':
                self.rect.x += PLAYER_STEPS
                self.direction = 'right'
            elif self.direction == 'right':
                self.rect.x -= PLAYER_STEPS
                self.direction = 'left'
            elif self.direction == 'up':
                self.rect.y += PLAYER_STEPS
                self.direction = 'down'
            elif self.direction == 'down':
                self.rect.y -= PLAYER_STEPS
                self.direction = 'up'
                
    def collide_player(self):
        collide = pygame.sprite.spritecollide(self, self._game.mainPlayer, True, pygame.sprite.collide_rect_ratio(0.9))
        
        if(collide):
            self._game._running = False
        

class Player_HealthBar(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self._game = game
        self._layer = HEALTH_LAYER
        self.groups = self._game._all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE
        
        self.width = 40
        self.height = 10
        
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)
        
        #determine position, want this to be at the top of the player on start
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y - TILE_SIZE/2 #just above player
        
    def damage(self, health, totalHealth):
        self.image.fill(RED)
        width = self.rect.width * health/totalHealth
        
        pygame.draw.rect(self.image, GREEN, (0,0,width, self.height), 0)
        
    def kill_bar(self):
        self.kill()
        
    def move(self):
        self.rect.x = self._game.player.rect.x
        self.rect.y = self._game.player.rect.y - TILE_SIZE/2
        
    def update(self):
        self.move()
        
class Enemy_HealthBar(pygame.sprite.Sprite):
    def __init__(self, game, enemy, x,y):
        self.enemy = enemy
        self._game = game
        self._layer = HEALTH_LAYER
        self.groups = self._game._all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x*TILE_SIZE
        self.y = y*TILE_SIZE
        
        self.width = 40
        self.height = 10
        
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)
        
        #determine position, want this to be at the top of the player on start
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y - TILE_SIZE/2 #just above player
        
    def move(self):
        self.rect.x = self.enemy.rect.x
        self.rect.y = self.enemy.rect.y - TILE_SIZE/2
        
    def damage(self, health, totalHealth):
        self.image.fill(RED)
        width = self.rect.width * health/totalHealth
        
        pygame.draw.rect(self.image, GREEN, (0,0,width, self.height), 0)
        
    def kill_bar(self):
        self.kill()
        
    def update(self):
        self.move()
        
class Particle(pygame.sprite.Sprite):
    def __init__(self, game, x,y):
        self._game = game
        self._layer = HEALTH_LAYER
        self.groups = self._game._all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface([4,4])
        self.image.fill((255,255,255))
        
        #determine position, want this to be at the top of the player on start
        self.rect = self.image.get_rect()
        self.rect.x = x + random.choice([-10,-5, -3, -1, 2, 3, 4, 10, 20, 30, 40])
        self.rect.y = y + TILE_SIZE
        self.lifetime = 6
        self.counter = 0
        
    def move(self):
        self.rect.y +=1
        self.counter += 1
        
        if self.counter == self.lifetime:
            self.counter = 0
            self.kill()
            
    def update(self):
        self.move()     