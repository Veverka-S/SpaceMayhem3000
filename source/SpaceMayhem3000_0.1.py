import sys
import random
import pygame as pg

###########################################################################################
#GAME_SPEEDS_AND_POSITIONS
resolution_x = 1650
resolution_y = 850

player_velocity_x = 7
player_velocity_y = 5

enemy_velocity_x = 3
enemy_velocity_y = 5

bullet_velocity = 10
bullet_count = 0

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

player = pg.image.load('obrazky/hrac.png').convert_alpha()
bullet = pg.image.load('obrazky/strela.png').convert_alpha()
enemy = pg.image.load('obrazky/nepritel.png').convert_alpha()
game_over = pg.image.load('obrazky/konec_hry.png').convert_alpha()

###########################################################################################
#GAME_CLASSES
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = player
        self.rect = self.image.get.rect()
        self.rect.center = resolution_x / 2
        self.rect.bottom = resolution_y - self.rect.height
        
        player_group.add(self)
        
        self.velocity_x = player_velocity_x
        self.velocity_y = player_velocity_y
        
        self.bullet_velocity = velocity
        self.bullet_count = 0
        
    def update(self):
        b = pygame.key.get_pressed()
        
        if b[K_UP] or b[K_w]:
            self.rect.y -= self.velocity_y
        if b[K_DOWN] or b[K_s]:
            self.rect.y += self.velocity_y
        if b[K_LEFT] or b[K_a]:
            self.rect.x -= self.velocity_x
        if b[K_RIGHT] or b[K_d]:
            self.rect.x += self.velocity_x
        
        self.bullet_count += 1
        
        if b[K_SPACE]:
            if self.bullet_count > self.bullet_velocity:
                Bullet(self)
                self.bullet_count = 0
        
        if self.rect.right > resolution_x:
            self.rect.right = resolution_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top > resolution_y:
            self.rect.top = resolution_y
        if self.rect.bottom < 0:
            self.rect.bottom = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        self.rect.y = player.rect.y
        
        Bullet_group.add(self)
        
        self.velocity = bullet_velocity
    def update(self):
        self.rect.y -= self.velocity
        
        if self.rect.y < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = enemy
        self.rect = self.image.get_rect()
        self.rect.y = random.randint(0, resolution_y /1.3)
        self.rect.x = random.randint(0, resolution_x - self.rect.width)
        
        enemy_group.add(self)
        
        self.velocity_y = enemy_velocity_y
    
    def update(self):
        
        self.rect.y += self.velocity.y
        self.rect.x -= self.velocity_x
        
        if self.rect.x > resolution_y - self.rect.width:
            self.velocity_x *= -1
        if self.rect.x < 0:
            self.velocity.x *= -1
        if self.rect.y > resolution_y - self.rect.height:
            self.velocity_y *= -1
        if self.rect.y < 0:
            self.velocity_y *= -1
###########################################################################################
#GAME_MENUS_AND_BUTTONS

def game_quit():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        