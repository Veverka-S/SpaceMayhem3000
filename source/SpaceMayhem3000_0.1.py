import sys
import random
import pygame as pg

pg.font.init()
###########################################################################################
#GAME_SPEEDS_AND_POSITIONS
resolution_x = 1650
resolution_y = 850

player_velocity_x = 15
player_velocity_y = 12

enemy_velocity_y = 1

bullet_velocity = 10
bullet_count = 0

max_enemy_endless_game = 3

player_health = 3

current_score = 0

max_enemy= 20
enemy_count = max_enemy

game_mode = 'menu'

enemy_spawn = True

spawn1 = True
spawn2 = True
spawn3 = True
spawn4 = True
spawn5 = True
spawn_boss = True


###########################################################################################
#GAME_SCREEN
pg.init()
pg.display.set_caption("Markovo Space Mayhem")
game = pg.display.set_mode((resolution_x, resolution_y))

###########################################################################################
#GAME_ASSETS
menu_bkg = pg.image.load('obrazky/menu_pozadi.jpg')
game_bkg = pg.image.load('obrazky/herni_pozadi.jpg')

play_button = pg.image.load('obrazky/tlacitko_play.jpg')
play_button_selected = pg.image.load('obrazky/tlacitko_play_vybrane.jpg')
credits_button = pg.image.load('obrazky/tlacitko_credits.jpg')
credits_button_selected = pg.image.load('obrazky/tlacitko_credits_vybrane.jpg')
quit_button = pg.image.load('obrazky/tlacitko_quit.jpg')
quit_button_selected = pg.image.load('obrazky/tlacitko_quit_vybrane.jpg')
endless_game_button = pg.image.load('obrazky/tlacitko_endless_game.jpg')
endless_game_button_selected = pg.image.load('obrazky/tlacitko_endless_game_vybrane.jpg')
career_button = pg.image.load('obrazky/career_button.jpg')
career_button_selected = pg.image.load('obrazky/career_button_selected.jpg')
exitsmall_button = pg.image.load('obrazky/EXIT_BUTTONSM.jpg')
exitsmall_button_selected = pg.image.load('obrazky/EXIT_BUTTONSMALL.jpg')
boss = pg.image.load('obrazky/boss.jpg')
credits_bkg = pg.image.load('obrazky/credits.jpg')

player = pg.image.load('obrazky/hrac.png').convert_alpha()
bullet = pg.image.load('obrazky/strela.png').convert_alpha()
enemy = pg.image.load('obrazky/nepritel.png').convert_alpha()
game_over = pg.image.load('obrazky/konec_hry.png').convert_alpha()
enemy_2 = pg.image.load('obrazky/konec_hry.png').convert_alpha()

###########################################################################################
#GAME_CLASSES
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = player
        self.rect = self.image.get_rect()
        self.rect.centerx = resolution_x / 2
        self.rect.bottom = resolution_y - self.rect.height / 2
        
        player_group.add(self)
        
        self.velocity_x = player_velocity_x
        self.velocity_y = player_velocity_y
        
        self.bullet_velocity = bullet_velocity
        self.bullet_count = 0
        
    def update(self):
        b = pg.key.get_pressed()
        
        if b[pg.K_UP] or b[pg.K_w]:
            self.rect.y -= self.velocity_y
        if b[pg.K_DOWN] or b[pg.K_s]:
            self.rect.y += self.velocity_y
        if b[pg.K_LEFT] or b[pg.K_a]:
            self.rect.x -= self.velocity_x
        if b[pg.K_RIGHT] or b[pg.K_d]:
            self.rect.x += self.velocity_x
        
        self.bullet_count += 1
        
        if b[pg.K_SPACE]:
            if self.bullet_count > self.bullet_velocity:
                Bullet(self)
                self.bullet_count = 0
        
        if self.rect.right > resolution_x:
            self.rect.right = resolution_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top > resolution_y - 50:
            self.rect.top = resolution_y - 50
        if self.rect.bottom < 0 + 50:
            self.rect.bottom = 0 + 50
class Boss(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = boss
        self.rect = self.image.get_rect()
        self.rect.x = resolution_x / 2 - 225
        self.rect.y = resolution_y / 2 - 225
        
        boss_group.add(self)
        
        player_group.add(self)
    
class Bullet(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        self.rect.y = player.rect.y
        
        bullet_group.add(self)
        
        self.velocity = bullet_velocity
    def update(self):
        self.rect.y -= self.velocity
        
        if self.rect.y < 0:
            self.kill()

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = enemy
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = random.randint(100, resolution_x - self.rect.width)
        while pg.sprite.spritecollide(self, enemy_group, False):
            self.rect.x = random.randint(0, resolution_x - self.rect.width)
            
        enemy_group.add(self)
        
        self.velocity_y = enemy_velocity_y
    
    def update(self):
        global current_score
        self.rect.y += self.velocity_y
        
        if self.rect.y > resolution_y:
            self.kill()
            if current_score > 0:
                current_score -= 75

class Enemy_BR(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = enemy
        self.rect = self.image.get_rect()
        self.rect.y = 100
        self.rect.x = 75
        while pg.sprite.spritecollide(self, enemy_group_br, False):
            self.rect.x += 75
            if self.rect.x > 1525:
                self.rect.x = 75
                self.rect.y += 100
            
        enemy_group_br.add(self)


###########################################################################################
#GAME_SPRITE_GROUPS
player_group = pg.sprite.Group()
enemy_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()
enemy_group_br = pg.sprite.Group()
enemy_group_br2 = pg.sprite.Group()
boss_group = pg.sprite.Group()
###########################################################################################
#GAME_MENUS_AND_BUTTONS

def game_quit():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    
    
def game_menu():
    global game_mode
    cursor = pg.mouse.get_pos()

    game.blit(menu_bkg,(0,0))
    game.blit(play_button,(400,100))
    game.blit(credits_button,(400,350))
    game.blit(quit_button,(400,600))

    if cursor[0] > 400 and cursor[0] < 1250 and cursor[1] > 100 and cursor[1] < 250:
        game.blit(play_button_selected, (400, 100))
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                game_mode = 'game_selection'

    elif cursor[0] > 400 and cursor [0] < 1250 and cursor[1]  > 350 and cursor[1] < 500:
        game.blit(credits_button_selected, (400, 350))
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                game_mode = 'credits'

    elif cursor[0] > 400 and cursor[0] < 1250 and cursor[1] > 600 and cursor[1] < 750:
        game.blit(quit_button_selected, (400, 600))       
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                exit()

def game_selection_menu():
    global game_mode
    cursor = pg.mouse.get_pos()

    game.blit(menu_bkg,(0,0))
    game.blit(endless_game_button,(400,250))
    game.blit(career_button,(400,500))

    if cursor[0] > 400 and cursor[0] < 1250 and cursor[1] > 250 and cursor[1] < 400:
        game.blit(endless_game_button_selected, (400, 250))
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                game_mode = 'endless_game'

    elif cursor[0] > 400 and cursor [0] < 1250 and cursor[1]  > 500 and cursor[1] < 650:
        game.blit(career_button_selected, (400, 500))
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                game_mode = 'boss_rush'


def zobrazeni_zivotu():
    if player_health > 3:
        font = pg.font.Font('freesansbold.ttf',30)
        s = "Health: " + str(player_health)
        text = font.render(s, 1, (255,255,255))
        game.blit(text,(20,20))
    if player_health == 3:
        font = pg.font.Font('freesansbold.ttf',30)
        s = "Health: " + str(player_health)
        text = font.render(s, 1, (255,255,255))
        game.blit(text,(20,20))
    elif player_health == 2:
        font = pg.font.Font('freesansbold.ttf',30)
        s = "Health: " + str(player_health)
        text = font.render(s, 1, (200,100,0))
        game.blit(text,(20,20))
    elif player_health == 1:
        font = pg.font.Font('freesansbold.ttf',30)
        s = "Health: " + str(player_health)
        text = font.render(s, 1, (255,0,0))
        game.blit(text,(20,20))
    
def game_over_screen():
    while True:
        m = pg.mouse.get_pos()
        game_quit()
        game.blit(menu_bkg,(0,0))
        game.blit(game_over,(0,0))
        game.blit(exitsmall_button,(1450, 50))
        font = pg.font.Font('freesansbold.ttf',60)
        s = "Your score was: " + str(current_score)
        text = font.render(s,1,(255,255,255))
        game.blit(text,(500, 700))
        
        if m[0] > 1450 and m[0] < 1550 and m[1] > 50 and m[1] < 100:
            game.blit(exitsmall_button_selected, (1450,50))
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    exit()
        
        pg.display.update()

def score():
    font = pg.font.Font('freesansbold.ttf',30)
    s = "Score: " + str(current_score)
    text = font.render(s,1,(255,255,255))
    game.blit(text,(20,65))

def endless_mode_accel():
    global max_enemy_endless_game
    global enemy_velocity_y
    if current_score > 1000 and current_score < 2500:
        enemy_velocity_y = 4
    
    if current_score > 2500  and current_score < 3500:
        max_enemy_endless_game = 6
        enemy_velocity_y = 3.75
    
    if current_score > 3500 and current_score < 4000:
        enemy_velocity_y = 4.25
    
    if current_score > 4000 and current_score < 11111112500:
        max_enemy_endless_game = 7
        enemy_velocity_y = 5

def hack_check():
    global current_score
    global player_health
    k = pg.key.get_pressed()
    
    if k[pg.K_o]:
        current_score += 10000
    if k[pg.K_p]:
        player_health += 1

###########################################################################################
player = Player()

while game_mode == 'menu':
    game_quit()
    game_menu()
    pg.display.update()

while game_mode == 'game_selection':
    game_quit()
    game_selection_menu()

    pg.display.update()
while game_mode == 'credits':
    game_quit()
    game.blit(credits_bkg,(0,0))
    pg.display.update()
    
while game_mode == 'endless_game':
    game_quit()
    if len(enemy_group.sprites()) < max_enemy_endless_game:
        Enemy()

    player_collided_with_enemy = pg.sprite.groupcollide(player_group, enemy_group, False, True)
    enemy_hit = pg.sprite.groupcollide(bullet_group, enemy_group, True, True)
    
    if player_collided_with_enemy:
        player_health -= 1
        if current_score > 0:
            current_score -= 100
        if player_health == 0:
            game_over_screen()
        
    if enemy_hit:
        current_score += 100
    
    game.blit(game_bkg,(0,0))
    
    player_group.update()
    enemy_group.update()
    bullet_group.update()
    
    player_group.draw(game)
    enemy_group.draw(game)
    bullet_group.draw(game)
    zobrazeni_zivotu()
    score()
    #hack_check()
    endless_mode_accel()
    
    pg.display.update()

while game_mode == 'boss_rush':

    game_quit()
    while enemy_spawn == True:
        if len(enemy_group_br.sprites()) < max_enemy:
            Enemy_BR()
            if len(enemy_group_br.sprites()) == max_enemy:
                enemy_spawn = False
       
    player_collided_with_enemy = pg.sprite.groupcollide(player_group, enemy_group_br, False, True)
    enemy_hit = pg.sprite.groupcollide(bullet_group, enemy_group_br, True, True)        

    if player_collided_with_enemy:
        player_health -= 1
        enemy_count -= 1
        if current_score > 0:
            current_score -= 100
            
    if player_health == 0:
        game_over_screen()
        
    if enemy_hit:
        current_score += 100
        enemy_count -= 1
        
    print(enemy_count)
    
    if enemy_count == 0 and spawn1 == True:
        max_enemy = 2
        enemy_count = max_enemy 
        enemy_spawn = True
        spawn1 = False

    
    if enemy_count == 0 and spawn2 == True:
        max_enemy = 3
        enemy_count = max_enemy 
        enemy_spawn = True
        spawn2 = False


    if enemy_count == 0 and spawn3 == True:
        max_enemy = 4
        enemy_count = max_enemy
        enemy_spawn = True
        spawn3 = False

        
    if enemy_count == 0 and spawn4 == True:
        max_enemy = 5
        enemy_count = max_enemy
        enemy_spawn = True
        spawn4 = False


    if enemy_count == 0 and spawn5 == True:
        max_enemy = 6
        enemy_count = max_enemy
        enemy_spawn = True
        spawn5 = False
    
    if enemy_count == 0 and spawn_boss == True:
        Boss()
        spawn_boss = False
 
    game.blit(game_bkg,(0,0))
    
    player_group.update()
    enemy_group_br.update()
    bullet_group.update()
    
    player_group.draw(game)
    enemy_group_br.draw(game)
    bullet_group.draw(game)
    zobrazeni_zivotu()
    score()
    
    pg.display.update()

    

