import pygame, sys, os, random #import pygame sys os and random

clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules
pygame.init() # initiates pygame
pygame.display.set_caption('Platformer MIPT edition') # set the window name

window_size = (600,400)

screen = pygame.display.set_mode(window_size,0,32) # initiate the screen

display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

true_scroll = [0,0] # how far the camera has moved

def load_map(path): # reading game map from text file
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame
        

animation_database = {}

animation_database['run'] = load_animation('player_animations/run',[7,7])
animation_database['idle'] = load_animation('player_animations/idle',[7,7,40])

game_map = load_map('map')

grass_img = pygame.image.load('grass.png')
tile_img = pygame.image.load('111.png')
scr_img = pygame.image.load('black.png')

jump_sound = pygame.mixer.Sound('jump.wav')
grass_sounds = [pygame.mixer.Sound('grass_1.wav'),pygame.mixer.Sound('grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

#pygame.mixer.music.load('music.wav')
#pygame.mixer.music.play(-1)

player_action = 'idle'
player_frame = 0
player_flip = False

grass_sound_timer = 0

player_rect = pygame.Rect(100,100,5,13)

background_objects = [[0.25,[7, 30, 20, 400]], [0.25,[70, 45, 50, 400]], [0.25,[150,10,70,400]],[0.25,[280, 30, 40, 400]],[0.5,[25, 50, 40,400]], [0.5,[130,75,100,400]], [0.5,[300,80,120,400]], [0.5,[450, 40, 65, 400]]]

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False} # dctionary of collisions
    if air_timer < 100 :
        rect.x += movement[0]
        hit_list = collision_test(rect,tiles) # list of all things player collides with
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
        hit_list = collision_test(rect,tiles) # collision check
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True

    else:
        rect.x += 0
        rect.y += 0
    return rect, collision_types

while True: # game loop
    display.fill((204, 255, 255)) # clear screen by filling it with blue

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display,(153, 76, 0),pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(0, 102, 204),obj_rect)
        else:
            pygame.draw.rect(display,(255, 255, 102),obj_rect)

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(tile_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '2':
                display.blit(grass_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1

    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_movement[0] > 0:
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,'run')
    if player_movement[0] < 0:
        player_flip = True
        player_action,player_frame = change_action(player_action,player_frame,'run')

    player_rect,collisions = move(player_rect,player_movement,tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
        if player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(grass_sounds).play()
    else:
        air_timer += 1
        #print(air_timer)

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))

    if air_timer > 100 :
        display.fill((0, 0, 0))

        #pygame.Rect(player_rect.x, player_rect.y, 100, 100)
        #f = pygame.font.Font(None, 35)
        #text = f.render('poluchaetsa akadem', 1, (255,255,255))
        #display.blit(text, (player_rect.x + 10, player_rect.y + 10)) 


        #f = pygame.font.Font(None, 50)
        #text = f.render('exit', 1,  (255, 255, 255))
        #screen.blit(text, (player_rect.x, player_rect.y))
    print(air_timer)
    print(player_rect.x, player_rect.y)



    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if (event.key == K_UP) or (event.key == pygame.K_SPACE):
                if air_timer < 6:
                    jump_sound.play()
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
        
    screen.blit(pygame.transform.scale(display,window_size),(0,0))
    pygame.display.update()
    clock.tick(60)
