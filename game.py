import pygame, sys
import random as r



class Tile():
    def __init__(self, img_t, pos):
        self.img_t = img_t
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

    def render(self, scroll, screen):
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

    def render(self, scroll, screen):
        if (self.visable == False):
            return
        if self.typee == "B":
            screen.blit(book1, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))
        if self.typee == "H":
            screen.blit(heart, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))
        if self.typee == "T1":
            screen.blit(treasure1, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))
        
    def collide_player(self, player, game):
        if self.visable == False:
            return [None]
        self.visable = False
        if self.typee == "B":
            player.current_items[0] = True
            return ["Learnt new skill: Knowledge Casting", 60]
        if self.typee == "H":
            player.player_health = min(player.player_health + 15, player.player_max_health)
            return ["Gained 15 health", 60]
        if self.typee == "T1":
            game.update_level(1, player)
            return ["Congradulations, you have completed level 1!", 60]
        return [None]

class Player():
    def __init__(self):
        self.player_vert_mom = 0
        self.player_horz_mom = 0
        self.player_size = [16, 32]
        self.player_rect = pygame.Rect(300, 200, self.player_size[0], self.player_size[1])
        self.player_items = [False]
        self.current_items = [False]
        self.current_level = 0
        self.player_dmg = 1
        self.player_health = 100
        self.player_max_health = 100
        self.moving_right, self.moving_left, self.facing_right = False, False, False
        self.in_air = True
        self.used_jump = False
        self.used_jump2 = False
        self.shooting_time = 0
        
        self.projectiles = []
    
    def shoot_proj(self):
        self.shooting_time = 20
        if self.current_items[0]:
            self.projectiles.append(Projectile("purple", (self.player_rect.x + 8, self.player_rect.y + 12), self.facing_right, 5))
            return
    

    def do_tick_and_render(self, level_tiles, level_items, level_enemies, scroll, screen, game):
        player_move_tick = [0, 0]
        messages = []

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
            new_message = level_items[x].collide_player(self, game)
            messages.append(new_message)

        colliding_enemies = check_enemy_collisions(self.player_rect, level_enemies)
        for x in colliding_enemies:
            new_message = level_enemies[x].collide_player(self)
            messages.append(new_message)
        
        
        
        for x in self.projectiles:
            x.update_and_render(screen, level_enemies, scroll)
        
        if self.player_health <= 0:
            messages = []
            messages.append(["Oh dear, you have died!", 60])
            self.level_start(self.current_level)
            game.update_level(self.current_level, self)
        
        if self.in_air:
            if self.facing_right:
                screen.blit(player_fall_img, (self.player_rect.x - scroll[0], self.player_rect.y - scroll[1]))
            else:
                screen.blit(pygame.transform.flip(player_fall_img, True, False), (self.player_rect.x - scroll[0], self.player_rect.y - scroll[1]))
        elif self.shooting_time > 0:
            self.shooting_time -= 1
            if self.facing_right:
                screen.blit(player_shoot_img, (self.player_rect.x - scroll[0], self.player_rect.y - scroll[1]))
            else:
                screen.blit(pygame.transform.flip(player_shoot_img, True, False), (self.player_rect.x - scroll[0], self.player_rect.y - scroll[1]))
        else:
            if self.facing_right:
                screen.blit(player_img, (self.player_rect.x - scroll[0], self.player_rect.y - scroll[1]))
            else:
                screen.blit(pygame.transform.flip(player_img, True, False), (self.player_rect.x - scroll[0], self.player_rect.y - scroll[1]))
        
        return messages
    
    def level_start(self, level):
        self.player_health = int(self.player_max_health)
        self.current_items = list(self.player_items)
        self.current_level = int(level)
    
    def level_end(self, level):
        self.player_items = list(self.current_items)

    def jump_handle(self):
        if self.used_jump and (not self.used_jump2):
            self.in_air = True
            self.player_vert_mom += -6.5
            self.used_jump2 = True
        elif (not self.used_jump) and (not self.used_jump2):
            self.player_vert_mom += -5.5
            self.in_air = True
        self.player_vert_mom = max(self.player_vert_mom, -3.5)
        self.used_jump = True
        

        

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
        
    def render(self, scroll, img, screen):
        screen.blit(img, (self.rect.x - scroll[0], self.rect.y - scroll[1]))

    def update_and_render(self, scroll, player, screen, level_tiles):
        if not self.alive:
            return
        if dist_to_player(self, player) < 400:   
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
                self.render(scroll, red_enemy_fall_img, screen)
            else:
                self.render(scroll, pygame.transform.flip(red_enemy_fall_img, True, False), screen)
        else:
            if self.moving_right:
                self.render(scroll, red_enemy_img, screen)
            else:
                self.render(scroll, pygame.transform.flip(red_enemy_img, True, False), screen)
    
    def collide_player(self, player):
        player.player_health -= 2
        if player.moving_right:
            player.player_horz_mom -= 3
        else:
            player.player_horz_mom += 3
        self.wait_timer = 30
        
        return [r.choice(["Ouch", "Yikes", "Oof", "Oueh", "Big oof"]), 30]

        
def dist_to_player(enemy, player):
    return abs(enemy.rect.x - player.player_rect.x)

def next_move_right(enemy, player):
    return (enemy.rect.x < player.player_rect.x)

                
class Button():
    def __init__(self, typee, img, pos):
        self.button_type = typee
        self.img = img
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], img.get_width(), img.get_height())

    def render(self, screen):
        screen.blit(self.img, self.pos)
    
    def click_checker(self, mouse_pos, game):
        if self.rect.collidepoint(mouse_pos):
            if self.button_type == "quit":
                game.quit_game()
            return True

class Projectile():
    def __init__(self, typee, pos, facing_right, speed):
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], 7, 7)
        self.typee = typee
        self.facing_right = True
        if facing_right:
            self.speed = speed
        else:
            self.speed = -speed
        
    
    def render(self, screen, scroll):
        if self.typee == "purple":
            if self.facing_right:
                screen.blit(purple_bullet_img, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
            else:
                screen.blit(pygame.transform.flip(purple_bullet_img, True, False), (self.rect.x - scroll[0], self.rect.y - scroll[1]))

        return

    def update_and_render(self, screen, enemy_list, scroll):
        tick_move = self.speed
        colliding_enemies = check_enemy_collisions(self.rect, level_enemies)
        messages = []
        for x in colliding_enemies:
            new_message = level_enemies[x].collide_player(self)
            messages.append(new_message)

        self.rect.x += tick_move
        self.render(screen, scroll)





background_img = pygame.image.load("img//background.png")
player_img = pygame.image.load("img//player.png")
player_fall_img = pygame.image.load("img//player_fall.png")
player_shoot_img = pygame.image.load("img//player_shoot.png")
grass = pygame.image.load("img//grass.png")
dirt = pygame.image.load("img//dirt.png")
book1 = pygame.image.load("img//book1.png")
red_enemy_img = pygame.image.load("img//red_enemy.png")
red_enemy_fall_img = pygame.image.load("img//red_enemy_fall.png")
heart = pygame.image.load("img//heart.png")
treasure1 = pygame.image.load("img//treasure1.png")
quit_img = pygame.image.load("img//exit.png")
purple_bullet_img = pygame.image.load("img//purple_bullet.png")

current_level = 0
level_tiles, level_items, level_enemies = [], [], []

class Game():
    def  __init__(self):
        pygame.init()
        self.level_tiles = []
        self.level_enemies = []
        self.level_items = []

        self.buttons = []

        self.win_height = 400
        self.win_width = 608
        self.display = (self.win_width, self.win_height)

        self.level_file_names = ["levels//1.txt", "levels//2.txt"]
        self.screen = pygame.display.set_mode(self.display, 0, 32)
        self.clock = pygame.time.Clock()

        self.current_level = 0
        self.player = Player()
    
    def make_level_data(self, levelnum):
        level_data = self.read_level(levelnum)
        self.level_tiles = []
        self.level_enemies = []
        self.level_items = []
        for x in enumerate(level_data):
            for y in enumerate(x[1]):
                #nothing
                if y[1] == "0":
                    continue
                #safe tiles
                if y[1] == "1":
                    self.level_tiles.append(Tile(y[1], (y[0]*16, x[0]*16)))
                if y[1] == "2":
                    self.level_tiles.append(Tile(y[1], (y[0]*16, x[0]*16)))
                #items
                if y[1] == "B":
                    self.level_items.append(Item(y[1], (y[0]*16, x[0]*16)))
                if y[1] == "H":
                    self.level_items.append(Item(y[1], (y[0]*16, x[0]*16)))
                if y[1] == "T":
                    self.level_items.append(Item("T1", (y[0]*16, x[0]*16)))
                #enemies
                if y[1] == "R":
                    self.level_enemies.append(Red_Enemy((y[0]*16, x[0]*16)))
                    

    def read_level(self, levelnum):
        filen = self.level_file_names[levelnum]
        grid = []
        with open(filen, "r") as filee:
            for x in enumerate(filee):
                grid.append([]) 
                row = x[1]
                for y in row:
                    grid[x[0]].append(y)
        return grid
    
    def quit_game(self):
        print("Game quit.")
        pygame.quit()
        sys.exit()

    def set_up_buttons(self):
        self.buttons.append(Button("quit", quit_img, (572, 5)))
    
    def button_check(self, mousepos):
        for x in self.buttons:
            x.click_checker(mousepos, self)

    def update_level(self, level, player): 
        player.level_end(level)
        self.make_level_data(level)
        self.current_level = level
        player.player_rect.x = 300
        player.player_rect.y = 200
        player.level_start(level)

    def main(self):
        pygame.display.set_caption("Treasure Hunter - Durham")

        self.set_up_buttons()

        messages = []
        count = True
        self.make_level_data(0)
        master_scroll = [0, 0]
        debug = True
        myfont = pygame.font.SysFont("Arial", 10)


        while True:
            self.screen.blit(background_img, (0,0))

            master_scroll[0] += (self.player.player_rect.x - master_scroll[0] - 150)
            master_scroll[1] += (self.player.player_rect.y - master_scroll[1] - 200)

            for x in self.level_tiles:
                x.render(master_scroll, self.screen)
            
            for x in self.level_items:
                x.render(master_scroll, self.screen)
            
            for x in self.level_enemies:
                x.update_and_render(master_scroll, self.player, self.screen, self.level_tiles)
            
            for x in self.buttons:
                x.render(self.screen)
            
            new_messages = self.player.do_tick_and_render(self.level_tiles, self.level_items, self.level_enemies, master_scroll, self.screen, self)
            for x in new_messages:
                if x != [None]:
                    messages.append(x)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.player.moving_right = True
                        self.player.facing_right = True
                    if event.key == pygame.K_a:
                        self.player.moving_left = True
                        self.player.facing_right = False
                    if event.key == pygame.K_w:
                        self.player.jump_handle()
                    if event.key == pygame.K_SPACE:
                        self.player.shoot_proj()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print("clicked at: ", pos)
                    button_pressed = False
                    for x in self.buttons:
                        button_pressed = x.click_checker(pos, game)
                    if not button_pressed:
                        pass # shoot
                        
                        

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.player.moving_right = False
                    if event.key == pygame.K_a:
                        self.player.moving_left = False
            
        
            
            
            if count % 100 == 0:
                print("tick", count)
            count+=1

    
            if debug:
                letter = myfont.render("fps: " + str(round(self.clock.get_fps(),2)),0,(0,0,0))
                self.screen.blit(letter,(0,0))
                letter = myfont.render("v_m: " + str(round(self.player.player_vert_mom,2)),0,(0,0,0))
                self.screen.blit(letter,(0,10))
                letter = myfont.render("h_m: " + str(round(self.player.player_horz_mom,2)),0,(0,0,0))
                self.screen.blit(letter,(0,20))
                letter = myfont.render("health: " + str(round(self.player.player_health,2)),0,(0,0,0))
                self.screen.blit(letter,(0,30))
                letter = myfont.render("player_level: " + str(round(self.player.current_level,2)),0,(0,0,0))
                self.screen.blit(letter,(0,40))
                letter = myfont.render("game_level: " + str(round(self.current_level,2)),0,(0,0,0))
                self.screen.blit(letter,(0,50))
                letter = myfont.render("items: " + str(self.player.current_items),0,(0,0,0))
                self.screen.blit(letter,(0,60))
            
            
           
            for x in enumerate(messages):
                letter = myfont.render(x[1][0],0,(0,0,0))
                self.screen.blit(letter, (self.player.player_rect.x - master_scroll[0] + 16, self.player.player_rect.y - master_scroll[1] + x[0]*10))
                x[1][1] -= 1
            
            for x in messages:
                if x[1] < 0:
                    messages.pop(messages.index(x))
            

            
            pygame.display.update()
            self.clock.tick(60)




        

       



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

#check if colliding with an enemy
def check_enemy_collisions(rectin, enemies):
    _, indexes = colliding_tiles(rectin, [enemy.rect for enemy in enemies])
    return indexes



game = Game()
game.main()

    
    
