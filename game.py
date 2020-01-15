import pygame, sys

debug = True
level_file_names = ["levels//1.txt"]

class Tile():
    def __init__(self, img_t, pos):
        self.img_t = img_t
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

    def render(self, scroll):
        if self.img_t == "1":
            screen.blit(grass, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))
        if self.img_t == "2":
            screen.blit(dirt, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))

class Item():
    def __init__(self, typee, pos):
        self.typee = typee
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        self.visable = True

    def render(self, scroll):
        if (self.visable == False):
            return
        if self.typee == "B":
            screen.blit(book1, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))
        if self.typee == "H":
            screen.blit(heart, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))
        if self.typee == "T1":
            screen.blit(treasure1, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))
        
    def collide_player(self, player):
        if self.visable == False:
            return
        self.visable = False
        if self.typee == "B":
            player.player_items[0] = True
        if self.typee == "H":
            player.player_health = min(player.player_health + 15, player.player_max_health)
        return

class Player():
    def __init__(self):
        self.player_vert_mom = 0
        self.player_horz_mom = 0
        self.player_size = [16, 32]
        self.player_rect = pygame.Rect(300, 200, self.player_size[0], self.player_size[1])
        self.player_items = [False]
        self.player_dmg = 1
        self.player_health = 100
        self.player_max_health = 100
        self.moving_right, self.moving_left, self.facing_right = False, False, False
        self.in_air = True
        self.used_jump, used_jump2 = False, False
        

    def do_tick_and_render(self, level_tiles, level_items, level_enemies, scroll):
        player_move_tick = [0, 0]

        if self.moving_left:
            self.player_horz_mom = max(self.player_horz_mom - 0.5, -3)
        elif self.moving_right:
            self.player_horz_mom = min(self.player_horz_mom + 0.5, 3)
        else:
            self.player_horz_mom = 0
        
        self.player_vert_mom = min(self.player_vert_mom + 0.2, 3)

        
            
        player_move_tick[0] += self.player_horz_mom
        player_move_tick[1] += self.player_vert_mom
        
    
    
        new_rect, collisions = check_collision_and_move(self.player_rect, [x.rect for x in level_tiles], player_move_tick)
        
        if (collisions[2] or collisions[3]):
            self.player_horz_mom = 0
        
    

        if collisions[1]:
            self.used_jump = False
            self.used_jump2 = False
            self.in_air = False
        
       
        colliding_items = check_item_collisions(self.player_rect, level_items)
        for x in colliding_items:
            level_items[x].collide_player(self)

        colliding_enemies = check_enemy_collisions(self.player_rect, level_enemies)
        for x in colliding_enemies:
            level_enemies[x].collide_player(self)
        
        if self.in_air:
            if self.facing_right:
                screen.blit(player_fall_img, (self.player_rect.x - scroll[0], self.player_rect.y - scroll[1]))
            else:
                screen.blit(pygame.transform.flip(player_fall_img, True, False), (self.player_rect.x - scroll[0], self.player_rect.y - scroll[1]))
        else:
            if self.facing_right:
                screen.blit(player_img, (self.player_rect.x - scroll[0], self.player_rect.y - scroll[1]))
            else:
                screen.blit(pygame.transform.flip(player_img, True, False), (self.player_rect.x - scroll[0], self.player_rect.y - scroll[1]))

class Red_Enemy():
    def __init__(self, pos):
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], 16, 32)
        self.alive = True
        self.in_air = False
        self.health = 10
        self.damage = 1
        self.moving_left = False
        self.moving_right = False
        self.vert_mom = False
        self.wait_timer = 0
        
    def render(self, scroll, img):
        screen.blit(img, (self.rect.x - scroll[0], self.rect.y - scroll[1]))

    def update_and_render(self, scroll, player):
        if not self.alive:
            return
        if dist_to_player(self, player) > 50:   
            move_tick = [0, 0]     
            move_right = next_move_right(self, player)
            if self.wait_timer == 0:
                if move_right:
                    self.moving_right = True
                    move_tick[0] += 1
                else:
                    self.moving_right = False
                    move_tick[0] -= 1
                
                self.vert_mom += 0.2
                if self.vert_mom > 3:
                    self.vert_mom = 3
            else:
                self.wait_timer -= 1
        
            move_tick[1] += self.vert_mom

            self.rect, collisions = check_collision_and_move(self.rect, [x.rect for x in level_tiles], move_tick)

            self.in_air = not collisions[1]
        
        
        if self.in_air:
            if self.moving_right:
                self.render(scroll, red_enemy_fall_img)
            else:
                self.render(scroll, pygame.transform.flip(red_enemy_fall_img, True, False))
        else:
            if self.moving_right:
                self.render(scroll, red_enemy_img)
            else:
                self.render(scroll, pygame.transform.flip(red_enemy_img, True, False))
    
    def collide_player(self, player):
        player.player_health -= 2
        if player.moving_right:
            player.player_horz_mom -= 3
        else:
            player.player_horz_mom += 3
        self.wait_timer = 30
        
        return 

        
def dist_to_player(enemy, player):
    return abs(enemy.rect.x - player.player_rect.x)

def next_move_right(enemy, player):
    return (enemy.rect.x < player.player_rect.x)


def make_level_data(levelnum):
    level_data = read_level(levelnum)
    level_tiles = []
    level_items = []
    level_enemies = []
    for x in enumerate(level_data):
        for y in enumerate(x[1]):
            #nothing
            if y[1] == "0":
                continue
            #safe tiles
            if y[1] == "1":
                level_tiles.append(Tile(y[1], (y[0]*16, x[0]*16)))
            if y[1] == "2":
                level_tiles.append(Tile(y[1], (y[0]*16, x[0]*16)))
            #items
            if y[1] == "B":
                level_items.append(Item(y[1], (y[0]*16, x[0]*16)))
            if y[1] == "H":
                level_items.append(Item(y[1], (y[0]*16, x[0]*16)))
            if y[1] == "T":
                level_items.append(Item("T1", (y[0]*16, x[0]*16)))
            #enemies
            if y[1] == "R":
                level_enemies.append(Red_Enemy((y[0]*16, x[0]*16)))
                
    
    return level_tiles, level_items, level_enemies


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

master_scroll = [0, 0]

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
red_enemy_img = pygame.image.load("img//red_enemy.png")
red_enemy_fall_img = pygame.image.load("img//red_enemy_fall.png")
heart = pygame.image.load("img//heart.png")
treasure1 = pygame.image.load("img//treasure1.png")



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



#check if colliding with an item
def check_item_collisions(rectin, items):
    _, indexes = colliding_tiles(rectin, [item.rect for item in items])
    return indexes

def check_enemy_collisions(rectin, enemies):
    _, indexes = colliding_tiles(rectin, [enemy.rect for enemy in enemies])
    return indexes



current_level = 0
level_tiles, level_items, level_enemies = make_level_data(current_level)
messages = []
count = True
player = Player()

while True:
    screen.blit(background_img, (0,0))

    master_scroll[0] += (player.player_rect.x - master_scroll[0] - 150)
    master_scroll[1] += (player.player_rect.y - master_scroll[1] - 200)

    for x in level_tiles:
        x.render(master_scroll)
    
    for x in level_items:
        x.render(master_scroll)
    
    for x in level_enemies:
        x.update_and_render(master_scroll, player)
    
    player.do_tick_and_render(level_tiles, level_items, level_enemies, master_scroll)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game quit.")
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.moving_right = True
                player.facing_right = True
            if event.key == pygame.K_a:
                player.moving_left = True
                player.facing_right = False
            if event.key == pygame.K_SPACE:
                if player.used_jump and (not player.used_jump2):
                    player.in_air = True
                    player.player_vert_mom += -6.5
                    player.used_jump2 = True
                elif (not player.used_jump) and (not player.used_jump2):
                    player.player_vert_mom += -5.5
                    player.in_air = True
                player.player_vert_mom = max(player.player_vert_mom, -3.5)
                player.used_jump = True
            if event.key == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.getpos()
                
                

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.moving_right = False
            if event.key == pygame.K_a:
                player.moving_left = False
    
  
    
    
    if count % 100 == 0:
        print("tick", count)
    count+=1

    myfont = pygame.font.SysFont("Arial", 10)
    if debug:
        letter = myfont.render("fps: " + str(round(clock.get_fps(),2)),0,(0,0,0))
        screen.blit(letter,(0,0))
        letter = myfont.render("v_m: " + str(round(player.player_vert_mom,2)),0,(0,0,0))
        screen.blit(letter,(0,10))
        letter = myfont.render("h_m: " + str(round(player.player_horz_mom,2)),0,(0,0,0))
        screen.blit(letter,(0,20))
        letter = myfont.render("health: " + str(round(player.player_health,2)),0,(0,0,0))
        screen.blit(letter,(0,30))
    
    for x in enumerate(messages):
        letter = myfont.render(x[1][0],0,(0,0,0))
        screen.blit(letter, (player.player_rect.x - master_scroll[0] + 16, player.player_rect.y - master_scroll[1] + x[0]*10))
        x[1][1] -= 1
    
    for x in messages:
        if x[1] == 0:
            messages.pop(messages.index(x))
    

    
    pygame.display.update()
    clock.tick(60)