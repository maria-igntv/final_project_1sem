import pygame, sys #import pygame and sys

clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules
pygame.init() # initiate pygame
pygame.display.set_caption('PLatformer MIPT edition') # set the window name

window_size = (700, 400) 

screen = pygame.display.set_mode(window_size, 0, 32) #initiate screen

bg = pygame.image.load('mipt_lk.jpg')
player_right = pygame.image.load('student_right.png')
player_left = pygame.image.load('student_left.png')
player_up_right = pygame.image.load('student_fr.png')
player_up_left = pygame.image.load('student_fl.png')

moving_right = False
moving_left = False
jump_left = False
jump_right = False

player_location = [50, 150]
player_y_momentum = 0

player_rect = pygame.Rect(player_location[0], player_location[1], player_right.get_width(), player_right.get_height())
test_rec = pygame.Rect(350, 100, 100, 50)

right = True # r l orientation of player

while True: #game loop
    
    screen.blit(bg,(0,0))
    if right == True:
        screen.blit(player_right, player_location)
    else:
        screen.blit(player_left, player_location)

    if player_location[1] > window_size[1] - player_right.get_height():
        player_y_momentum = -player_y_momentum
    else:
        player_y_momentum += 0.2
    player_location[1] += player_y_momentum

    if moving_right == True:
        right = True
        player_location[0] += 4

    if moving_left == True:
        right = False
        player_location[0] -= 4

    if jump_left == True:
        right = False
        player_location[1] += 4

    if jump_right == True:
        right = True
        player_location[1] += 4


    player_rect.x = player_location[0]
    player_rect.y = player_location[1]

    if player_rect.colliderect(test_rec):
        pygame.draw.rect(screen, (255, 0, 0), test_rec)
    else:
        pygame.draw.rect(screen, (255, 255, 255), test_rec)
        

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
               # if air_timer < 6:
                    player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    pygame.display.update()
    clock.tick(100)
