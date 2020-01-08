import pygame, sys
from pygame import *

def read_level(filen):
    grid = []
    with open(filen, "r") as filee:
        for x in enumerate(filee):
            grid.append([]) 
            row = x[1].strip().split(",")
            for y in row:
                grid[x[0]].append(y)
    return grid

    

win_height = 400
win_width = 608
display = (win_width, win_height)

pygame.init()
pygame.display.set_caption("Treasure Hunter - Durham")

screen = pygame.display.set_mode(display, 0, 32)
clock = pygame.time.Clock()

background = pygame.image.load("img//background.png")
player = pygame.image.load("img//player.png")
player.set_colorkey((255,255,255))
grass = pygame.image.load("img//grass.png")
dirt = pygame.image.load("img//dirt.png")

player_vert_mom = 0
player_rect = pygame.Rect(50, 50, player.get_width(), player.get_height())

moving_right, moving_left = False, False

#check if colliding with list of tiles
def colliding_tiles(rectin, tiles):
    colliding_tiles = []
    for x in tiles:
        if rectin.colliderect(x):
            colliding_tiles.append(x)
    return colliding_tiles

#check if collision after moving (tiles)
def check_collision_and_move(rectin, tiles, movement):
    rectin.x += movement[0]
    collding_with = colliding_tiles(rectin, tiles)
    for x in collding_with:
        if movement[0] > 0:
            rectin.right = x.left 
        elif movement[0] < 0:
            rectin.left = x.right
    
    rectin.y += movement[1]
    collding_with = colliding_tiles(rectin, tiles)

    for x in collding_with:
        if movement[1] > 0:
            rectin.bottom = x.top 
        elif movement[1] < 0:
            rectin.top = x.bottom

    return rectin

current_level = read_level("levels//1.txt")

while True:
    screen.blit(background, (0,0))
    screen.blit(player, (player_rect.x, player_rect.y))

    level_tiles = []

    for x in enumerate(current_level):
        for y in enumerate(x[1]):
            if y[1] == "0":
                continue
            if y[1] == "1":
                screen.blit(grass, (y[0]*16, x[0]*16))
            if y[1] == "2":
                screen.blit(dirt, (y[0]*16, x[0]*16))
            level_tiles.append(pygame.Rect(y[0]*16, x[0]*16, 16, 16))

    player_move_tick = [0, 0]

    if moving_left:
        player_move_tick[0] -= 3
    if moving_right:
        player_move_tick[0] += 3
    
    player_vert_mom += 0.2
    if player_vert_mom > 2:
        player_vert_mom = 2

    player_move_tick[1] += player_vert_mom

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
            if event.key == K_SPACE:
                player_vert_mom += -5

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    player_rect = check_collision_and_move(player_rect, level_tiles, player_move_tick)

    
    pygame.display.update()
    clock.tick(60)