import pygame
import random
import sys


resolution_x = 1650 
resolution_y = 850 
pohled = pygame.display.set_mode((resolution_x,resolution_y))
pygame.init()
#Programy
#POSOTIONS
playerx = 825
playery = 725
enemyx = random.randint(0,1630)
enemyy = random.randint(0,700)
shotv = 15
vv = 5
hv = 7
def mov():
    global playerx
    global playery
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        playery -= vv
    if key[pygame.K_DOWN]:
        playery += vv
    if key[pygame.K_LEFT]:
        playerx -= hv
    if key[pygame.K_RIGHT]:
        playerx += hv
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sship.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y ):
        self.image = pygame.image.load('shot.png').convert_alpha()
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



    
def exitbutton():
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            quit()




        

#Když se level rovná 0, tak se otevře menu

#GRAFIKA
pygame.display.set_caption("Markovo Space Mayhem")
bkg = pygame.image.load('bkg.jpg')
play = pygame.image.load('play.jpg')
credit = pygame.image.load('credits.jpg')
end = pygame.image.load('quit.jpg')
plays = pygame.image.load('plays.jpg')
creditss = pygame.image.load('creditss.jpg')
quits = pygame.image.load('quits.jpg')
game = pygame.image.load('game.jpg')
sship = pygame.image.load('sship.png').convert_alpha()
game_over = pygame.image.load('game_over.png').convert_alpha()

white = (255, 255, 255)

#uroven
level = 0

#pocet zivotu
lives = 3

move = True


while level == 0:
    
    exitbutton()
    pohled.fill(white)
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
while level == 1:
    exitbutton()
    pohled.blit(game,(0,0))
    shotx = playerx - 6.5
    shoty = playery - 15
    v = 15
    
    enemy = Enemy([enemyx,enemyy])
    enemy_group = pygame.sprite.Group()
    enemy_group.add(enemy)
    
    player = Player([playerx, playery])
    player_group = pygame.sprite.Group()
    player_group.add(player)
    
    shot = Bullet(shotx,shoty)
    shot_group = pygame.sprite.Group()
    shot_group.add(shot)

    player_group.draw(pohled)
    enemy_group.draw(pohled)
    key = pygame.key.get_pressed()
    
    if move == True:
        enemyy += 1
    
    if move == True:
        mov()
    collision_with_enemy = pygame.sprite.spritecollide(player, enemy_group, True, pygame.sprite.collide_rect_ratio(0.7))
    if collision_with_enemy:
        move = False
        pohled.blit(game_over,(0,0))
    if key[pygame.K_SPACE]:
        shot_group.draw(pohled)
    
    if playerx > 1625:
        playerx = 1625
    if playerx < 25:
        playerx = 25
    if playery > 825:
        playery = 825
    if playery < 25:
        playery = 25

            
    
    
    
    
    
    pygame.display.update()
