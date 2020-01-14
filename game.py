import pygame, sys
from pygame import *

level_file_names = ["levels//1.txt"]

class tile():
    def __init__(self, img_t, pos):
        self.img_t = img_t
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

    def render(self, scroll):
        if self.img_t == "1":
            screen.blit(grass, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))
        if self.img_t == "2":
            screen.blit(dirt, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))

class item():
    def __init__(self, t, pos):
        self.t = t
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        self.visable = True

    def render(self, scroll):
        if (self.visable == False):
            return
        if self.t == "B":
            screen.blit(book1, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))
        
    def oncollide(self, player_rect):
        self.visable = False
        if self.t == "B":
            player_items[0] = True
        return



def make_level_data(levelnum):
    level_data = read_level(levelnum)
    level_tiles = []
    level_items = []
    for x in enumerate(level_data):
        for y in enumerate(x[1]):
            #nothing
            if y[1] == "0":
                continue
            #safe tiles
            if y[1] == "1":
                level_tiles.append(tile(y[1], (y[0]*16, x[0]*16)))
            if y[1] == "2":
                level_tiles.append(tile(y[1], (y[0]*16, x[0]*16)))
            #items
            if y[1] == "B":
                level_items.append(item(y[1], (y[0]*16, x[0]*16)))
    
    return level_tiles, level_items


def read_level(levelnum):
    filen = level_file_names[levelnum]
    grid = []
    with open(filen, "r") as filee:
        for x in enumerate(filee):
            grid.append([]) 
            row = x[1]
            for y in row:
                grid[x[0]].append(y)
    return grid


win_height = 400
win_width = 608
display = (win_width, win_height)

scroll = [0, 0]

pygame.init()
pygame.display.set_caption("Treasure Hunter - Durham")

screen = pygame.display.set_mode(display, 0, 32)
clock = pygame.time.Clock()

background_img = pygame.image.load("img//background.png")
player_img = pygame.image.load("img//player.png")
player_fall_img = pygame.image.load("img//player_fall.png")
grass = pygame.image.load("img//grass.png")
dirt = pygame.image.load("img//dirt.png")
book1 = pygame.image.load("img//book1.png")

player_vert_mom = 0
player_size = [16, 32]
player_rect = pygame.Rect(300, 200, player_size[0], player_size[1])
player_items = [False]

moving_right, moving_left, facing_right = False, False, False
in_air = True
used_jump, used_jump2 = False, False

#check if colliding with list of tiles
def colliding_tiles(rectin, tiles):
    colliding_tiles = []
    indexes = []
    for x in enumerate(tiles):
        if rectin.colliderect(x[1]):
            colliding_tiles.append(x[1])
            indexes.append(x[0])
    return colliding_tiles, indexes

#check if collision after moving (tiles)
def check_collision_and_move(rectin, tiles, movement):
    collisions = [False, False, False, False]
    #top, bottom, left, right
    rectin.x += movement[0]
    collding_with, _ = colliding_tiles(rectin, tiles)
    for x in collding_with:
        if movement[0] > 0:
            rectin.right = x.left
            collisions[3] = True
        elif movement[0] < 0:
            rectin.left = x.right
            collisions[2] = True
    
    rectin.y += movement[1]
    collding_with, _ = colliding_tiles(rectin, tiles)

    for x in collding_with:
        if movement[1] > 0:
            rectin.bottom = x.top 
            collisions[1] = True
        elif movement[1] < 0:
            rectin.top = x.bottom
            collisions[0] = True

    return rectin, collisions

def check_item_collisions(rectin, items):
    _, indexes = colliding_tiles(rectin, [items.rect for items in items])
    return indexes


current_level = 0
level_tiles, level_items = make_level_data(current_level)
    
count = True
while True:
    screen.blit(background_img, (0,0))

    scroll[0] += (player_rect.x - scroll[0] - 150)
    scroll[1] += (player_rect.y - scroll[1] - 200)

    for x in level_tiles:
        x.render(scroll)
    
    for x in level_items:
        x.render(scroll)

    player_move_tick = [0, 0]

    if moving_left:
        player_move_tick[0] -= 3
    if moving_right:
        player_move_tick[0] += 3
    
    player_vert_mom += 0.2
    if player_vert_mom > 3:
        player_vert_mom = 3

    player_move_tick[1] += player_vert_mom

    rects = [x.rect for x in level_tiles]
    

    player_rect, collisions = check_collision_and_move(player_rect, [x.rect for x in level_tiles], player_move_tick)

    if collisions[1]:
        used_jump = False
        used_jump2 = False
        in_air = False
    
    colliding_items = check_item_collisions(player_rect, level_items)
    for x in colliding_items:
        level_items[x].oncollide(player_rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            print("Game quit.")
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
                facing_right = True
            if event.key == K_a:
                moving_left = True
                facing_right = False
            if event.key == K_SPACE:
                if used_jump and (not used_jump2):
                    in_air = True
                    player_vert_mom += -6.5
                    used_jump2 = True
                elif (not used_jump) and (not used_jump2):
                    player_vert_mom += -5.5
                    in_air = True
                player_vert_mom = max(player_vert_mom, -3.5)
                used_jump = True
            if event.key == MOUSEBUTTONDOWN:
                pos = pygame.mouse.getpos()
                
                

        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False
    
    if in_air:
        if facing_right:
            screen.blit(player_fall_img, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
        else:
            screen.blit(pygame.transform.flip(player_fall_img, True, False), (player_rect.x - scroll[0], player_rect.y - scroll[1]))
    else:
        if facing_right:
            screen.blit(player_img, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
        else:
            screen.blit(pygame.transform.flip(player_img, True, False), (player_rect.x - scroll[0], player_rect.y - scroll[1]))

        
    
    
    if count % 100 == 0:
        print("tick", count)
    count+=1

    myfont = pygame.font.SysFont("Arial", 10)
    letter = myfont.render("fps: " + str(round(clock.get_fps(),2)),0,(0,0,0))
    screen.blit(letter,(0,0))
    letter = myfont.render("v_m: " + str(round(player_vert_mom,2)),0,(0,0,0))
    screen.blit(letter,(0,10))

    
    pygame.display.update()
    clock.tick(60)