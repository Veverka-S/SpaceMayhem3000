import sys
import random
import pygame as pg

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

max_enemy = 5

player_health = 3

current_score = 0

button_width = 850
button_height = 150

game_mode = 'menu'
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
designs_button = pg.image.load('obrazky/designs_button.jpg')
designs_button_selected = pg.image.load('obrazky/designs_button_selected.jpg')

player = pg.image.load('obrazky/hrac.png').convert_alpha()
bullet = pg.image.load('obrazky/strela.png').convert_alpha()
enemy = pg.image.load('obrazky/nepritel.png').convert_alpha()
game_over = pg.image.load('obrazky/konec_hry.png').convert_alpha()

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
        self.rect.x = random.randint(0, resolution_x - self.rect.width)
        
        enemy_group.add(self)
        
        self.velocity_y = enemy_velocity_y
    
    def update(self):
        
        self.rect.y += self.velocity_y
        
        if self.rect.y > resolution_y:
            self.kill()
###########################################################################################
#GAME_SPRITE_GROUPS
player_group = pg.sprite.Group()
enemy_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()
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
    game.blit(endless_game_button,(400,100))
    game.blit(career_button,(400,350))
    game.blit(designs_button,(400,600))

    if cursor[0] > 400 and cursor[0] < 1250 and cursor[1] > 100 and cursor[1] < 250:
        game.blit(endless_game_button_selected, (400, 100))
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                game_mode = 'endless_game'

    elif cursor[0] > 400 and cursor [0] < 1250 and cursor[1]  > 350 and cursor[1] < 500:
        game.blit(career_button_selected, (400, 350))
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                game_mode = 'boss_rush'

    elif cursor[0] > 400 and cursor[0] < 1250 and cursor[1] > 600 and cursor[1] < 750:
        game.blit(designs_button_selected, (400, 600))       
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                game_mod = 'designs'

def zobrazeni_zivotu():
    if player_health == 3:
        font = pg.font.Font(None,25)
        s = "Health: " + str(player_health)
        text = font.render(s, 1, (255,255,255))
        game.blit(text,(0,0))
    elif player_health == 2:
        font = pg.font.Font(None,25)
        s = "Health: " + str(player_health)
        text = font.render(s, 1, (200,100,0))
        game.blit(text,(0,0))
    elif player_health == 1:
        font = pg.font.Font(None,25)
        s = "Health: " + str(player_health)
        text = font.render(s, 1, (255,0,0))
        game.blit(text,(0,0))
    
def game_over_screen():
    while True:
        game_quit()
        game.blit(menu_bkg,(0,0))
        game.blit(game_over,(0,0))
        font = pg.font.Font(None,50)
        s = "Your score was: " + str(current_score)
        text = font.render(s,1,(255,255,255))
        game.blit(text,(500, 700))
        pg.display.update()

def score():
    font = pg.font.Font(None,25)
    s = "Score: " + str(current_score)
    text = font.render(s,1,(255,255,255))
    game.blit(text,(0,25))

def endless_mode_accel():
    global max_enemy_endless_game
    global enemy_velocity_y
    if current_score == 1000 or current_score == 1050 :
        enemy_velocity_y += 0.25
    
    if current_score == 2500 or current_score == 2550:
        max_enemy_endless_game += 1
        enemy_velocity_y += 0.25

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

while game_mode == 'endless_game':
    game_quit()
    if len(enemy_group.sprites()) < max_enemy_endless_game:
        Enemy()

    player_collided_with_enemy = pg.sprite.groupcollide(player_group, enemy_group, False, True)
    enemy_hit = pg.sprite.groupcollide(bullet_group, enemy_group, True, True)
    
    if player_collided_with_enemy:
        player_health -= 1
        current_score -= 50
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
    endless_mode_accel()
    
    pg.display.update()
    
    
    
    



        