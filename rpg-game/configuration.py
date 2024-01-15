MIN_WIDTH = 640
MIN_HEIGHT = 640
TILE_SIZE = 32 #in pixels
FPS = 60
PLAYER_STEPS = 3 #how many pixels 
ENEMY_STEPS = 1

#layer order
GROUND_LAYER = 1
BLOCKS_LAYER = 2
ENEMY_LAYER = 3
PLAYER_LAYER = 4


#colors
BLACK = (0,0,0)

#20x20 
#B is block
#. is empty area
#each tile will 
tilemap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B...BBB................W.....B',
    'B.....W...................E..B',
    'B.....W......................B',
    'B...................BBB......B',
    'B.....E..............BB......B',
    'B............................B',
    'B......BBB.................E.B',
    'B.........P..................B',
    'B....E..............W........B',
    'B..................WW........B',
    'B........................E...B',
    'B......BBBB..................B',
    'B...W....BB..............WW..B',
    'B...................B....WW..B',
    'B......BB..........BB........B',
    'B....E..................E....B',
    'B....................BBBBB...B',
    'B....E....................E..B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]