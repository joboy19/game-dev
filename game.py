import pygame, sys
import random as r
import math as math



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
        if self.typee.startswith("T"):
            screen.blit(treasure1, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))
        if self.typee.startswith("P"):
            screen.blit(page_img, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))
        if self.typee == "G":
            screen.blit(gold_heart_img, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))
            
        
    def collide_player(self, player, game):
        if self.visable == False:
            return [None]
        self.visable = False
        if self.typee == "B":
            player.current_items[0] = True
            return ["Book of Knowledge! Press SPACE.", 60]
        if self.typee == "H":
            player.player_health = min(player.player_health + 15, player.player_max_health)
            return ["Gained 15 health", 60]
        if self.typee == "T0":
            game.level_data[1] = True
            if game.level_data == [True, True]:
                game.update_level(1, player)
                return ["Congradulations, you have completed level 1!", 60]#
            else:
                return ["Now you need the knowledge page!", 60]
        if self.typee == "P0":
            player.upgrade_player(1)
            game.level_data[0] = True
            if game.level_data == [True, True]:
                game.update_level(1, player)
                return ["Congradulations, you have completed level 1!", 60]#
            else:
                return ["Now you need the treasure!", 60]
        if self.typee == "T1":
            game.level_data[1] = True
            if game.level_data == [True, True]:
                game.update_level(2, player)
                return ["Congradulations, you have completed level 2!", 60]#
            else:
                return ["Now you need the knowledge page!", 60]
        if self.typee == "P1":
            player.upgrade_player(1)
            game.level_data[0] = True
            if game.level_data == [True, True]:
                game.update_level(2, player)
                return ["Congradulations, you have completed level 2!", 60]#
            else:
                return ["Now you need the treasure!", 60]
        if self.typee == "T2":
            game.level_data[1] = True
            if game.level_data == [True, True]:
                game.update_level(2, player)
                return ["Congradulations, you have completed level 3!", 60]#
            else:
                return ["Now you need the knowledge page!", 60]
        if self.typee == "P2":
            player.upgrade_player(1)
            game.level_data[0] = True
            if game.level_data == [True, True]:
                game.update_level(2, player)
                return ["Congradulations, you have completed level 3!", 60]#
            else:
                return ["Now you need the treasure!", 60]
        if self.typee == "T3":
            game.level_data[1] = True
            if game.level_data == [True, True]:
                game.update_level(2, player)
                return ["Congradulations, you have completed level 4!", 60]#
            else:
                return ["Now you need the knowledge page!", 60]
        if self.typee == "P3":
            player.upgrade_player(1)
            game.level_data[0] = True
            if game.level_data == [True, True]:
                game.update_level(2, player)
                return ["Congradulations, you have completed level 4!", 60]#
            else:
                return ["Now you need the treasure!", 60]

        if self.typee == "G":
            player.upgrade_player(2)
        return [None]

class HUD():
    def __init__(self):
        self.display = True
    def draw(self, screen, player):
        myfont = pygame.font.SysFont("Helvetica", 15, bold=True)
        letter = myfont.render("Level: " + str(player.current_level),0,(0,0,0))
        screen.blit(letter,(0,15))
        letter = myfont.render("Health: " + str(player.player_health) + "/" + str(player.player_max_health),0,(0,0,0))
        screen.blit(letter,(0,30))
        letter = myfont.render("Damage: " + str(player.player_dmg),0,(0,0,0))
        screen.blit(letter,(0,45))
        



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
        self.messages = []
    
    def upgrade_player(self, typee):
        if typee == 1:
            self.player_dmg *= 2
            self.messages.append(["Your damage has increase!", 60])
        if typee == 2:
            self.player_max_health += 25
            self.messages.append(["Your max health has increase!", 60])
    
    def shoot_proj(self):
        if len(self.projectiles) >= 3:
            self.messages.append(["You can only shoot 3 bullets at once", 10])
            return
        if self.current_items[0]:
            self.shooting_time = 20
            self.projectiles.append(Projectile("purple", (self.player_rect.x + 8, self.player_rect.y + 12), self.facing_right, 5, self.player_dmg))
            return
    
    def render_messages(self, screen, scroll):
        myfont = pygame.font.SysFont("Arial", 10)
        for x in enumerate(self.messages):
            letter = myfont.render(x[1][0],0,(0,0,0))
            screen.blit(letter, (self.player_rect.x - scroll[0] + 18, self.player_rect.y - scroll[1] + x[0]*10))
            x[1][1] -= 1
        for x in self.messages:
            if x[1] < 0:
                self.messages.pop(self.messages.index(x))
    

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
            if new_message != [None]:
                self.messages.append(new_message)

        colliding_enemies = check_enemy_collisions(self.player_rect, level_enemies)
        for x in colliding_enemies:
            new_message = level_enemies[x].collide_player(self)
            if new_message != [None]:
                self.messages.append(new_message)
        
        
        
        for x in self.projectiles:
            if not x.update_and_render(screen, level_enemies, level_tiles, scroll):
                self.projectiles.pop(self.projectiles.index(x))
        
        if self.player_health <= 0:
            self.messages = []
            self.messages.append(["Oh dear, you have died!", 60])
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
        
        self.render_messages(screen, scroll)
        return
    
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
        self.messages = []
        self.particles = []
        
    def render(self, scroll, img, screen):
        screen.blit(img, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
    
    def hit(self, damage):
        self.health -= damage
        self.messages = []
        self.messages.append(["Health: " + str(self.health), 10])
        self.wait_time = 10
        for x in range(10):
            self.particles.append(Magic_Particle((self.rect.x, self.rect.y+16), (128, 0, 128)))
    
    def render_messages(self, screen, scroll):
        myfont = pygame.font.SysFont("Arial", 10)
        for x in enumerate(self.messages):
            letter = myfont.render(x[1][0],0,(0,0,0))
            screen.blit(letter, (self.rect.x - scroll[0] + 18, self.rect.y - scroll[1] + x[0]*10))
            x[1][1] -= 1
        for x in self.messages:
            if x[1] < 0:
                self.messages.pop(self.messages.index(x))

    def update_and_render(self, scroll, player, screen, level_tiles):
        if self.health <= 0:
            self.alive = False
        if not self.alive:
            return False
        if dist_to_player(self, player) == 400:
            self.messages.append(["You will not get our knowledge!", 120])
        if dist_to_player(self, player) <= 400:   
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
        
        
        for x in self.particles:
            if not x.update(screen, scroll):
                self.particles.pop(self.particles.index(x))
        
        self.render_messages(screen, scroll)
        return True
    
    def collide_player(self, player):
        player.player_health -= self.damage
        if player.moving_right:
            player.player_horz_mom -= 3
        else:
            player.player_horz_mom += 3
        self.wait_timer = 30
        
        return [r.choice(["Ouch", "Yikes", "Oof", "Oueh"]), 30]

class Blue_Enemy():
    def __init__(self, pos):
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], 16, 32)
        self.alive = True
        self.in_air = False
        self.health = 50
        self.damage = 1
        self.moving_left = False
        self.moving_right = False
        self.vert_mom = False
        self.wait_timer = 0
        self.messages = []
        self.particles = []
        
    def render(self, scroll, img, screen):
        screen.blit(img, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
    
    def hit(self, damage):
        self.health -= damage
        self.messages = []
        self.messages.append(["Health: " + str(self.health), 10])
        self.wait_time = 10
        for x in range(10):
            self.particles.append(Magic_Particle((self.rect.x, self.rect.y+16), (128, 0, 128)))
    
    def render_messages(self, screen, scroll):
        myfont = pygame.font.SysFont("Arial", 10)
        for x in enumerate(self.messages):
            letter = myfont.render(x[1][0],0,(0,0,0))
            screen.blit(letter, (self.rect.x - scroll[0] + 18, self.rect.y - scroll[1] + x[0]*10))
            x[1][1] -= 1
        for x in self.messages:
            if x[1] < 0:
                self.messages.pop(self.messages.index(x))

    def update_and_render(self, scroll, player, screen, level_tiles):
        if self.health <= 0:
            self.alive = False
        if not self.alive:
            return False
        if dist_to_player(self, player) == 400:
            self.messages.append(["How dare you step foot here!", 120])
        if dist_to_player(self, player) <= 400:   
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
                self.vert_mom = min(self.vert_mom, 3)
                self.vert_mom = max(self.vert_mom, -2)
            else:
                self.wait_timer -= 1
        
            move_tick[1] += self.vert_mom

            self.rect, collisions = check_collision_and_move(self.rect, [x.rect for x in level_tiles], move_tick)

            self.in_air = not collisions[1]
            if collisions[2] or collisions[3]:
                self.vert_mom -= 5
        
        
        if self.in_air:
            if self.moving_right:
                self.render(scroll, blue_enemy_fall_img, screen)
            else:
                self.render(scroll, pygame.transform.flip(blue_enemy_fall_img, True, False), screen)
        else:
            if self.moving_right:
                self.render(scroll, blue_enemy_img, screen)
            else:
                self.render(scroll, pygame.transform.flip(blue_enemy_img, True, False), screen)
        
        
        for x in self.particles:
            if not x.update(screen, scroll):
                self.particles.pop(self.particles.index(x))
        
        self.render_messages(screen, scroll)
        return True
    
    def collide_player(self, player):
        player.player_health -= self.damage
        if player.moving_right:
            player.player_horz_mom -= 3
        else:
            player.player_horz_mom += 3
        self.wait_timer = 30
        
        return [r.choice(["Ouch", "Yikes", "Oof", "Oueh"]), 30]


        
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
    def __init__(self, typee, pos, facing_right, speed, damage):
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], 7, 7)
        self.typee = typee
        self.facing_right = True
        self.damage = damage
        if facing_right:
            self.speed = speed
        else:
            self.speed = -speed
        self.alive = True
        self.alive_time = 0
        
    
    def render(self, screen, scroll):
        if self.typee == "purple":
            if self.facing_right:
                screen.blit(purple_bullet_img, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
            else:
                screen.blit(pygame.transform.flip(purple_bullet_img, True, False), (self.rect.x - scroll[0], self.rect.y - scroll[1]))

        return

    def update_and_render(self, screen, level_enemies, level_tiles, scroll):
        if not self.alive:
            return False
        if self.alive_time > 40:
            self.alive = False
            return False
        tick_move = self.speed

        colliding_enemies = check_enemy_collisions(self.rect, level_enemies)
        for x in colliding_enemies:
            level_enemies[x].hit(self.damage)
            self.alive = False
        
        _, collision = check_collision_and_move(self.rect, [x.rect for x in level_tiles], (tick_move, 0))
        if True in collision:
            print("here")
            self.alive = False



        self.rect.x += tick_move
        self.render(screen, scroll)
        self.alive_time += 1
        return True

class Magic_Particle():
    def __init__(self, location, colour):
        self.x = location[0]
        self.y = location[1]
        angle = r.random()*6.28 - 3.14
        self.weightx = math.sin(angle)
        self.weighty = math.cos(angle)
        self.colour = colour
        self.timer = 50
    def update(self, screen, scroll):
        self.x += 0.4 * self.weightx
        self.y += 0.4 * self.weighty
        self.timer -= 1
        if self.timer >= 0:
            self.render(screen, scroll)
            return True
        return False
    def render(self, screen, scroll):
        pygame.draw.rect(screen, self.colour, pygame.Rect(self.x - scroll[0], self.y - scroll[1], 1, 2))

        


background_img = pygame.image.load("img//background.png")
menu = pygame.image.load("img//menu.png")
player_img = pygame.image.load("img//player.png")
player_fall_img = pygame.image.load("img//player_fall.png")
player_shoot_img = pygame.image.load("img//player_shoot.png")
grass = pygame.image.load("img//grass.png")
dirt = pygame.image.load("img//dirt.png")
book1 = pygame.image.load("img//book1.png")
red_enemy_img = pygame.image.load("img//red_enemy.png")
red_enemy_fall_img = pygame.image.load("img//red_enemy_fall.png")
blue_enemy_img = pygame.image.load("img//blue_enemy.png")
blue_enemy_fall_img = pygame.image.load("img//blue_enemy_fall.png")
heart = pygame.image.load("img//heart.png")
gold_heart_img = pygame.image.load("img//heart_gold.png")
treasure1 = pygame.image.load("img//treasure1.png")
quit_img = pygame.image.load("img//exit.png")
purple_bullet_img = pygame.image.load("img//purple_bullet.png")
page_img = pygame.image.load("img//page.png")

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

        self.level_file_names = ["levels//1.txt", "levels//2.txt", "levels//3.txt"]
        self.screen = pygame.display.set_mode(self.display, 0, 32)
        self.clock = pygame.time.Clock()

        self.current_level = 0
        self.player = Player()

        self.level_data = [False, False]
    
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
                    self.level_items.append(Item("T" + str(levelnum), (y[0]*16, x[0]*16)))
                if y[1] == "P":
                    self.level_items.append(Item("P" + str(levelnum), (y[0]*16, x[0]*16)))
                if y[1] == "G":
                    self.level_items.append(Item(y[1], (y[0]*16, x[0]*16)))

                #enemies
                if y[1] == "R":
                    self.level_enemies.append(Red_Enemy((y[0]*16, x[0]*16)))
                if y[1] == "J":
                    self.level_enemies.append(Blue_Enemy((y[0]*16, x[0]*16)))
                    

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
        self.level_data = [False, False]
    
    def intro(self):
        text = "The year is 2520, Durham and it's univserity has all but been destroyed. A cult of knowledge b-" \
               "earers have set up a small but powerful civilisation within the ruins of the university and ha-" \
               "ve stopped all access to what remains of the knowledge to the rest of the world. There is litt-" \
               "le time before they can permanently seal off the knowledge to the rest of the world.           " \
               "You are the last hope, before humanity loses all access to the knowledge left in the remains.  " \
               "You must collect 5 hidden treasure chests, to use as a bribe and 5 hidden pages of knowledge,  " \
               "well treasured by the cult, which can be placed in a book of knowledge which harnesses the     " \
               "knowledge and lets you use them to fight back. Each page will make you stronger, 5 strong      " \
               "enough to defeat their leader.                                                                 "
        count = 95
        myfont = pygame.font.SysFont("Arial", 15)
        repeat = True
        num_lines = 1
            
        while repeat:
            if count == 0:
                num_lines += 1
                count = 95
            elif num_lines <= 9:
                count -= 1
            

            for x in range(num_lines):
                letter = myfont.render(text[x*95:(x+1)*95-count],0,(255,255,255))
                self.screen.blit(letter,(0,60 + (x*15)))

            letter = myfont.render("[Press any key to skip]",0,(255,255,255))
            self.screen.blit(letter,(0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    repeat = False
            
            pygame.display.update()
            self.clock.tick(60)
        
        repeat = True
        while repeat:
            letter = myfont.render("[Press any key to start]",0,(255,255,255))
            self.screen.blit(letter,(0,0))
            self.screen.blit(menu, (0,0))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    repeat = False

            pygame.display.update()
            self.clock.tick(60)



            
            


    def main(self):
        pygame.display.set_caption("Treasure Hunter - Durham")

        self.intro()

        self.set_up_buttons()

        messages = []
        count = True
        self.make_level_data(0)
        master_scroll = [0, 0]
        debug = False
        myfont = pygame.font.SysFont("Arial", 10)
        hud = HUD()


        while True:
            self.screen.blit(background_img, (0,0))

            master_scroll[0] += (self.player.player_rect.x - master_scroll[0] - 150)
            master_scroll[1] += (self.player.player_rect.y - master_scroll[1] - 200)

            for x in self.level_tiles:
                x.render(master_scroll, self.screen)
            
            for x in self.level_items:
                x.render(master_scroll, self.screen)
            
            for x in self.level_enemies:
                if not x.update_and_render(master_scroll, self.player, self.screen, self.level_tiles):
                    self.level_enemies.pop(self.level_enemies.index(x))
            
            for x in self.buttons:
                x.render(self.screen)
            
            self.player.do_tick_and_render(self.level_tiles, self.level_items, self.level_enemies, master_scroll, self.screen, self)

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
            
            hud.draw(self.screen, self.player)
            
           
            
            
            
            

            
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

    
    
