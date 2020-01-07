import pygame, sys
from pygame import *

win_height = 600
win_width = 800
display = (win_width, win_height)

pygame.init()
pygame.display.set_caption("Treasure Hunter - Durham")

screen = pygame.display.set_mode(display, 0, 32)
clock = pygame.time.Clock()

background = pygame.image.load("img//background.png")
player = pygame.image.load("img//player.png")
player.set_colorkey((255,255,255))

player_location = [50, 50]
player_y_mom = 0
player_rect = pygame.Rect(player_location[0], player_location[1], player.get_width(), player.get_height())

moving_right, moving_left = False, False


while True:

    screen.blit(background, (0,0))

    screen.blit(player, player_location)

    if moving_left:
        player_location[0] -= 1
    if moving_right:
        player_location[0] += 1
    
    if player_location[1] >= win_height - player.get_height():
        player_location[1] = win_height - player.get_height()
    else:
        player_y_mom += 0.2
        player_location[1] += player_y_mom

    player_rect.x = player_location[0]
    player_rect.y = player_location[1]


    for event in pygame.event.get():

        if event.type == QUIT:
            print("Quitting...")
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    
    pygame.display.update()
    clock.tick(60)