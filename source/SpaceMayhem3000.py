import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
#Informace lode
vv = 5 #vertical_velocity
hv = 7 #horizontal_velocity
sshipx = 800 #pozice x
sshipy = 750 #pozice y
sshipw=50 #sirka
sshiph=50 #vyska
#obrazovka
resolution_x = 1650
resolution_y = 850
#dimenze tlacitek
selectionx = 500
selectiony = 65
selectionh = 200
selectionw = 650
#pozice zlacitka play
playx = 500
playy = 65
#pozice tlacitka credits
creditsx = 500
creditsy = 330
#pozice tlacitka quit
quitx = 500
quity = 595
rocketx = 255
rockety = 637
movspeed = 15
#uroven
level = 0
#existence rakety
rocket = False
#pocet zivotu
health = 3
#enemy
max_enemy = 8
max_velikost_enemy = 50
max_sirka_enemy = 50

pohled = pygame.display.set_mode((resolution_x,resolution_y))

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
shot = pygame.image.load('shot.png').convert_alpha()
sship = pygame.image.load('sship.png').convert_alpha()
pygame.transform.scale(sship,(25,25))

#Programy
def exitbutton():
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            quit()

def ovladani_lodi():
    global sshipy
    global sshipx
    if key[pygame.K_w]:
        sshipy -= vv
        if sshipy < 0:
            sshipy = 0
    if key[pygame.K_s]:
        sshipy += vv
        if sshipy > resolution_y - sshiph:
            sshipy = resolution_y - sshiph
    if key[pygame.K_a]:
        sshipx -= hv
        if sshipx < 0:
            sshipx = 0
    if key[pygame.K_d]:
        sshipx += hv
        if sshipx > resolution_x - sshipw:
            sshipx = resolution_x - sshipw

enemies = []
for i in range(max_enemy):
    enemy = dict()
    
    enemy['w'] = 50
    enemy['h'] = enemy['w']
    
    enemy['x'] = random.randint(0, resolution_x - enemy['w'])
    enemy['y'] = random.randint(0, resolution_y - enemy['h'] - 150)
    enemy['rgb'] = (random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))
    
    enemies.append(enemy)
                                
            
#Když se level rovná 0, tak se otevře menu
while level == 0:
    exitbutton()
    pohled.fill(white)
    pohled.blit(bkg, (0,0))
    pohled.blit(play, (selectionx,selectiony))
    pohled.blit(credit, (selectionx, selectiony*2 + selectionh))
    pohled.blit(end, (selectionx, selectiony*3 + selectionh*2))
    cursor = pygame.mouse.get_pos()
    
    if cursor[0] > 500 and cursor[0] < 1150 and cursor[1] > 65 and cursor[1] < 265:
        pohled.blit(plays,(playx,playy))
        if pygame.mouse.get_pressed()[0]:
            # level se nastaví na 1, což je hra
            level = 1
    elif cursor[0] > 500 and cursor [0] < 1150 and cursor[1]  > 330 and cursor[1] < 550:
        pohled.blit(creditss,(creditsx,creditsy))
        if pygame.mouse.get_pressed()[0]:
            #bud se dodělávat později, potřebuji zjistit jak vyčíst ze souboru.
            pass
    elif cursor[0] > 500 and cursor[0] < 1150 and cursor[1] > 615 and cursor[1] < 815:
        pohled.blit(quits,(quitx,quity))
        if pygame.mouse.get_pressed()[0]:
            exit()
    pygame.display.update()
while level == 1:
    exitbutton()
    pohled.fill(white)
    pohled.blit(game, (0,0))
    pohled.blit(sship, (sshipx,sshipy))
    key = pygame.key.get_pressed()
    ovladani_lodi()
    for enemy in enemies:
        pygame.draw.ellipse(pohled, enemy['rgb'], (enemy['x'], enemy['y'], enemy['w'], enemy['h']))
            

            
    
    
    
    
    
    pygame.display.update()
