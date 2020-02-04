import pygame
import random
import sys


dis_width = 1650 
dis_height = 850 
pohled = pygame.display.set_mode((dis_width,dis_height))
pygame.init()
move = True 
#POSOTIONS
enemyx = random.randint(0,1600)
enemyy = random.randint(0,700)
shot_velocity = 15
rate_of_fire = 3
ship_vv = 5
ship_hv = 7
ship_x = 825
ship_y = 725

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, v):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.y = x
        self.y = y
        self.v = v
        
    def move(self):
        if move == True:
            global enemy_v
            self.y -= self.v
            self.rect.y = self.y



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/sship.png').convert_alpha()
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y = y
        self.x = x
        
    def mov():
        if move == True:
            global ship_x
            global ship_y
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]:
                ship_y -= ship_vv
            if key[pygame.K_DOWN]:
                ship_y += ship_vv
            if key[pygame.K_LEFT]:
                ship_x -= ship_hv
            if key[pygame.K_RIGHT]:
                ship_x += ship_hv
            if ship_x > dis_width - 50:
                ship_x = dis_width - 50
            if ship_x < 0:
                ship_x = 0
            if ship_y > dis_height - 50:
                ship_y = dis_height - 50
            if ship_y < 0:
                ship_y = 0
                
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/shot.png').convert_alpha()
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        
    def move(self):
        if move == True:
            self.y -= shot_velocity
            self.rect.y = self.y

    
def exitbutton():
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            quit()
            
def collision_detection():
    collision_with_enemy = pygame.sprite.spritecollide(player, enemy_group, True, pygame.sprite.collide_rect_ratio(0.7))
    
    if collision_with_enemy:
        move = False
        pohled.blit(game_over,(0,0))

def menu_buttons():
    global level
    pohled.blit(bkg, (0,0)) #pozadí
    pohled.blit(play, (500,65)) #tlacitko_play
    pohled.blit(credit, (500, 330)) #tlacitko_credits
    pohled.blit(end, (500, 595)) #tlacitko_quit
    
    cursor = pygame.mouse.get_pos()
    
    if cursor[0] > 500 and cursor[0] < 1150 and cursor[1] > 65 and cursor[1] < 265:
        pohled.blit(plays,(500,65))
        if pygame.mouse.get_pressed()[0]:
            level = 1
    elif cursor[0] > 500 and cursor [0] < 1150 and cursor[1]  > 330 and cursor[1] < 550:
        pohled.blit(creditss,(500,330))
        if pygame.mouse.get_pressed()[0]:
            #bud se dodělávat později, potřebuji zjistit jak vyčíst ze souboru.
            pass
    elif cursor[0] > 500 and cursor[0] < 1150 and cursor[1] > 615 and cursor[1] < 815:
        pohled.blit(quits,(500,595))
        if pygame.mouse.get_pressed()[0]:
            exit()
    pygame.display.update()



        

#Když se level rovná 0, tak se otevře menu

#GRAFIKA
pygame.display.set_caption("Markovo Space Mayhem")
bkg = pygame.image.load('assets/bkg.jpg')
play = pygame.image.load('assets/play.jpg')
credit = pygame.image.load('assets/credits.jpg')
end = pygame.image.load('assets/quit.jpg')
plays = pygame.image.load('assets/plays.jpg')
creditss = pygame.image.load('assets/creditss.jpg')
quits = pygame.image.load('assets/quits.jpg')
game = pygame.image.load('assets/game.jpg')
sship = pygame.image.load('assets/sship.png').convert_alpha()
game_over = pygame.image.load('assets/game_over.png').convert_alpha()

white = (255, 255, 255)

#uroven
level = 0

#pocet zivotu
lives = 3

shots = []
rate_count = 0
enemies = []

enemy_v = 5

move = True


while level == 0:
    
    exitbutton()
    menu_buttons()
    pygame.display.update()
    
while level == 1:
    exitbutton()
    pohled.blit(game,(0,0))
    
    enemy_x = random.randint(0, dis_width - 50)
    enemy_y = random.randint(0, dis_height - 50)
    shotx = ship_x + 18
    shoty = ship_y
    
    max_enemies = 10
    
    #GENERACE HRACE
    player = Player(ship_x, ship_y)
    player_group = pygame.sprite.Group()
    player_group.add(player)
    
    enemy = Enemy(enemy_x, enemy_y, 15)
    enemy_group = pygame.sprite.Group()
    enemy_group.add(enemy)
    enemy_group.draw(pohled)
    
    shot_group = pygame.sprite.Group()

    player_group.draw(pohled)
    
    key = pygame.key.get_pressed()
    
    #POHYB HRACE - FINALNI VERZE
    Player.mov()
    
        
    #STRILENI
    shot = Bullet(shotx,shoty)
    if key[pygame.K_SPACE] and rate_count > rate_of_fire:
        shots.append(shot)
        rate_count = 0
        bullets_on_screen = 0
    else:
        rate_count += 1
    
    for shot in shots:
        shot.move()
        enemy_killed = pygame.sprite.spritecollide(shot, enemy_group, True, pygame.sprite.collide_rect_ratio(0.5))
        if not enemy_killed:
            if shot.y < 0:
                shots.remove(shot)
            else:
                shot_group.add(shot)
        else:
            move = False
    else:
        shot_group.draw(pohled)
    
    collision_detection()
 
    pygame.display.update()
