MIN_WIDTH = 640
MIN_HEIGHT = 640
TILE_SIZE = 32 #in pixels
FPS = 60
PLAYER_STEPS = 3 #how many pixels 
ENEMY_STEPS = 1
BULLET_STEPS = 6

#layer order
GROUND_LAYER = 1
BLOCKS_LAYER = 2
ENEMY_LAYER = 3
WEAPONS_LAYER = 4
PLAYER_LAYER = 5
HEALTH_LAYER = 6


#colors
BLACK = (0,0,0)
GREEN = (0,255,0)

#20x20 
#B is block
#. is empty area
#each tile will 
tilemap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B...BBB......I.........W.....B',
    'B.....W...................E..B',
    'B.....W......................B',
    'B..........I........BBB......B',
    'B.....E..............BB......B',
    'B...............I............B',
    'B......BBB.................E.B',
    'B.........P..I...............B',
    'B....E..............W.....I..B',
    'B..................WW........B',
    'B........................E...B',
    'B......BBBB..................B',
    'B...W....BB..............WW..B',
    'B...................B....WW..B',
    'B......BB..........BB........B',
    'B....E.........I........E....B',
    'B....................BBBBB...B',
    'B....E....................E..B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]