# pouzite baliky/knihovny
import sys
import random
import pygame

# inicializace
pygame.init()
okno = pygame.display.set_mode((1650, 850))
pygame.display.set_caption("Markovo Space Mayhem")

# parametry aplikace
pozice_hrace_x = 825
pozice_hrace_y = 725

rychlost_hrace_y = 5
rychlost_hrace_x = 7

rychlost_strely = 15
rychlost_strelby = 5

zivoty_hrace = 3

max_pocet_nepratel = 3
rychlost_nepratel = 3

# pomocne tridy
class Hrac(pygame.sprite.Sprite):
    def __init__(self, pozice_x, pozice_y):
        pygame.sprite.Sprite.__init__(self)

        self.image = textura_hrac
        
        self.rect = self.image.get_rect()
        self.rect.x = pozice_x
        self.rect.y = pozice_y
        
        vykreslovani_hraci.add(self)
        
        self.rychlost_x = rychlost_hrace_x
        self.rychlost_y = rychlost_hrace_y
        
        self.rychlost_strelby = rychlost_strelby
        self.pocitadlo_strelby = 0
        
    def update(self):
        key = pygame.key.get_pressed()
        
        if key[pygame.K_UP]:
            self.rect.y -= self.rychlost_y
        if key[pygame.K_DOWN]:
            self.rect.y += self.rychlost_y
        if key[pygame.K_LEFT]:
            self.rect.x -= self.rychlost_x
        if key[pygame.K_RIGHT]:
            self.rect.x += self.rychlost_x
        
        if self.rect.x > 1625:
            self.rect.x = 1625
        if self.rect.x < 25:
            self.rect.x = 25
        if self.rect.y > 825:
            self.rect.y = 825
        if self.rect.y < 25:
            self.rect.y = 25

        self.pocitadlo_strelby += 1
        
        if key[pygame.K_SPACE]:
            if self.pocitadlo_strelby > self.rychlost_strelby:
                Strela(self)
                self.pocitadlo_strelby = 0

class Strela(pygame.sprite.Sprite):
    def __init__(self, hrac):
        self.image = textura_strela
        
        pygame.sprite.Sprite.__init__(self)
        
        self.rect = self.image.get_rect()
        self.rect.x = hrac.rect.center[0] - self.rect.width / 2
        self.rect.y = hrac.rect.center[1] - 15
        
        vykreslovani_strely.add(self)
        
        self.rychlost = rychlost_strely
        
    def update(self):
        self.rect.y -= self.rychlost
        
        if self.rect.y < 0:
            self.kill()

class Nepritel(pygame.sprite.Sprite):
    def __init__(self, pozice_x, pozice_y):
        self.image = texture_nepritel
        
        pygame.sprite.Sprite.__init__(self)
        
        self.rect = self.image.get_rect()
        self.rect.x = pozice_x
        self.rect.y = pozice_y
        
        vykreslovani_nepratele.add(self)
        
        self.rychlost = rychlost_nepratel
    
    def update(self):
        self.rect.y += self.rychlost
        
        if self.rect.y > 850:
            self.kill()

# pomocne funkce
def zkontrolovat_vypnuti_hry():
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            quit()
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.quit()
        quit()

def zobrazit_menu():
    okno.fill((255, 255, 255))
    okno.blit(pozadi_menu, (0, 0))
    okno.blit(tlacitko_play, (500, 65))
    okno.blit(tlacitko_credits, (500, 330))
    okno.blit(tlacitko_quit, (500, 595))

def zobrazit_konec_hry():
    okno.blit(textura_konec, (0, 0))
    
    while True:
        zkontrolovat_vypnuti_hry()
        
        pygame.display.update()

def vybrat_z_menu():
    global rezim_hry
    
    cursor = pygame.mouse.get_pos()
    
    if cursor[0] > 500 and cursor[0] < 1150 and cursor[1] > 65 and cursor[1] < 265:
        okno.blit(tlacitko_play_vybrano, (500, 65))
        
        if pygame.mouse.get_pressed()[0]:
            rezim_hry = 'hra'
    elif cursor[0] > 500 and cursor [0] < 1150 and cursor[1]  > 330 and cursor[1] < 550:
        okno.blit(tlacitko_credits_vybrano, (500, 330))
        
        if pygame.mouse.get_pressed()[0]:
            pass
    elif cursor[0] > 500 and cursor[0] < 1150 and cursor[1] > 615 and cursor[1] < 815:
        okno.blit(tlacitko_quit_vybrano, (500, 595))
        
        if pygame.mouse.get_pressed()[0]:
            exit()

# herni assety
pozadi_menu = pygame.image.load('assets/bkg.jpg')
pozadi_hra = pygame.image.load('assets/game.jpg')

tlacitko_play = pygame.image.load('assets/play.jpg')
tlacitko_play_vybrano = pygame.image.load('assets/plays.jpg')
tlacitko_credits = pygame.image.load('assets/credits.jpg')
tlacitko_credits_vybrano = pygame.image.load('assets/creditss.jpg')
tlacitko_quit = pygame.image.load('assets/quit.jpg')
tlacitko_quit_vybrano = pygame.image.load('assets/quits.jpg')

textura_hrac = pygame.image.load('assets/sship.png').convert_alpha()
textura_strela = pygame.image.load('assets/shot.png').convert_alpha()
texture_nepritel = pygame.image.load('assets/enemy.png').convert_alpha()

textura_konec = pygame.image.load('assets/game_over.png').convert_alpha()

# zacatek programu
vykreslovani_hraci = pygame.sprite.Group()
vykreslovani_strely = pygame.sprite.Group()
vykreslovani_nepratele = pygame.sprite.Group()

hrac = Hrac(pozice_hrace_x, pozice_hrace_y)

rezim_hry = 'menu'

while rezim_hry == 'menu':
    zkontrolovat_vypnuti_hry()
    
    zobrazit_menu()
    vybrat_z_menu()

    pygame.display.update()

while rezim_hry == 'hra':
    zkontrolovat_vypnuti_hry()
    
    okno.blit(pozadi_hra,(0,0))
    
    if len(vykreslovani_nepratele.sprites()) < max_pocet_nepratel:
        Nepritel(random.randint(0,1630), 0)

    pygame.sprite.groupcollide(vykreslovani_nepratele, vykreslovani_strely, True, True)
    
    if pygame.sprite.groupcollide(vykreslovani_hraci, vykreslovani_nepratele, False, True):
        zivoty_hrace -= 1
        
        if zivoty_hrace == 0:
            zobrazit_konec_hry()

    vykreslovani_hraci.update()
    vykreslovani_strely.update()
    vykreslovani_nepratele.update()
    
    vykreslovani_hraci.draw(okno)
    vykreslovani_strely.draw(okno)
    vykreslovani_nepratele.draw(okno)
    
    pygame.display.update()
