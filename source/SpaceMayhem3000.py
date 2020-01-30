import pygame
import time

pygame.init()

white = (255, 255, 255)
#obrazovka
X = 1650
Y = 850
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
#herni pozadi
gamex = 0
gamey = -850
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
#vybrane tlacitko v menu
selected = 1

pohled = pygame.display.set_mode((X,Y))

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

def exitbutton():
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            quit()
#Když se level rovná 0, tak se otevře menu
while level == 0:
    exitbutton()
    pohled.fill(white)
    pohled.blit(bkg, (0,0))
    pohled.blit(play, (selectionx,selectiony))
    pohled.blit(credit, (selectionx, selectiony*2 + selectionh))
    pohled.blit(end, (selectionx, selectiony*3 + selectionh*2))
    cursor = pygame.mouse.get_pos()
    mpress = pygame.key.get_pressed()
    
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
    #když hru spustím v tomto stavu, tak funguje menu a dá se klikat
    #ale když přidám while level == 1:, tak se vytvoří blackscreen, někdy se dokonce objeví i menší pruh na okraji obrazovky

    pygame.display.update()
while level == 1:
    exitbutton()
    pohled.fill(white)
    pohled.blit(bkg, (0,0))

    pygame.display.update()
quit()
