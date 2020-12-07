import pygame, sys #import pygame and sys

clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules
pygame.init() # initiate pygame
pygame.display.set_caption('PLatformer MIPT edition') # set the window name

window_size = [550, 400] 

screen = pygame.display.set_mode(window_size, 0, 32) #initiate screen

display = pygame.Surface(window_size)

bg = pygame.image.load('mipt_lk.jpg')

tile_img = pygame.image.load('111.png')
tile_size = tile_img.get_width()
grass_img = pygame.image.load('grass.jpg')
grass_size = grass_img.get_width()

player_right = pygame.image.load('student_right.png')
#player_right.set_colorkey((255, 255, 255))
player_left = pygame.image.load('student_left.png')
player_up_right = pygame.image.load('student_fr.png')
player_up_left = pygame.image.load('student_fl.png')

game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0', '0', '0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0', '0', '0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0', '0', '0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0', '0', '0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0', '0', '0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0', '0', '0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0', '0', '0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0', '0', '0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0', '0', '0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0', '0', '0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0', '0', '0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0', '0', '0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0', '0', '0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0', '0', '0', '0'],
            ['1','1','1','1','2','2','2','2','0','0','0','0','0','0','0','0','2','2','2', '2', '2', '2'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1', '1', '1', '1'],
            ]

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move (rect, movement, tiles): # movement is a list of 2 values x and y
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False} # dctionary of collisions
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles) # list of all things player collides with
    for tile in hit_list:
        # update the players position x axis
        if movement[0] > 0: # moving right
            rect.right = tile.left 
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True

        # update the players position by y axis
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles) # collision check
    for tile in hit_list:
        if movement[1] > 0: # falling down
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

moving_right = False
moving_left = False
jump_left = False
jump_right = False

#player_location = [50, 150]
player_y_momentum = 0
air_timer = 0

player_rect = pygame.Rect(50, 50, player_right.get_width(), player_right.get_height())
test_rec = pygame.Rect(350, 100, 100, 50)

right = True # r l orientation of player
up = False

while True: #game loop
    
    display.blit(bg,(0,0))

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(tile_img, (x*tile_size , y*tile_size)) # tile if 1
            if tile == '2':
                display.blit(grass_img, (x*grass_size, y*grass_size)) # grass if 2
            if tile != '0':
                tile_rects.append(pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size)) # spacce
            x += 1
        y += 1


    '''
    # bouncing
    if player_location[1] > window_size[1] - player_right.get_height():
        player_y_momentum = -player_y_momentum
    else:'''

    player_movement = [0, 0] # how much we intend to move the player
    if moving_right:
        player_movement[0] += 2 # incresing velocity
    if moving_left:
        player_movement[0] -= 2

    player_movement[1] += player_y_momentum # gravity
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3 # can't fall faster than 3 sec

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1


    if (right == True) and (up == False):
        display.blit(player_right, (player_rect.x, player_rect.y))
    elif (right == True) and (up == True):
        display.blit(player_up_right, (player_rect.x, player_rect.y))

    elif (right == False) and (up == False):
        display.blit(player_left, (player_rect.x, player_rect.y))
    elif (right == False) and (up == True):
        display.blit(player_up_left, (player_rect.x, player_rect.y))

   # if player_location[1] > window_size[1] - player_right.get_height():
    #    player_location[1] = window_size[1] - player_right.get_height()

    if moving_right == True:
        right = True
        player_movement[0] += 4

    if moving_left == True:
        right = False
        player_movement[0] -= 4

    if jump_left == True:
        up = True
        right = False
        player_movement[1] += 4

    if jump_right == True:
        up = True
        right = True
        player_movement[1] += 4

    if player_rect.colliderect(test_rec):
        pygame.draw.rect(display, (255, 0, 0), test_rec)
    else:
        pygame.draw.rect(display, (255, 255, 255), test_rec)
        

    for event in pygame.event.get():
        if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if (event.key == K_UP) or (event.key == pygame.K_SPACE)    :
                up = True
                if air_timer < 6:
                    player_y_momentum = -4  
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            if (event.key == pygame.K_SPACE) or (event.key == K_UP):
                up = False 

    surf = pygame.transform.scale(display, window_size)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(100)
