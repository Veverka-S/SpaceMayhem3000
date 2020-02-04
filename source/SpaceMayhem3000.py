# pouzite baliky/knihovny
import sys
import random
import pygame

# parametry aplikace
velikost_okna_x = 1650
velikost_okna_y = 850

rychlost_hrace_y = 5
rychlost_hrace_x = 7

zivoty_hrace = 3

rychlost_strely = 15
rychlost_strelby = 5

max_pocet_nepratel = 3
rychlost_nepratel = 3

# inicializace
pygame.init()

okno = pygame.display.set_mode((velikost_okna_x, velikost_okna_y))
pygame.display.set_caption("Markovo Space Mayhem")

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
textura_nepritel = pygame.image.load('assets/enemy.png').convert_alpha()
textura_konec_hry = pygame.image.load('assets/game_over.png').convert_alpha()

# pomocne tridy
class Hrac(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = textura_hrac
        
        self.rect = self.image.get_rect()
        self.rect.centerx = velikost_okna_x / 2
        self.rect.bottom = velikost_okna_y - self.rect.height / 2
        
        vykreslovaci_skupina_hrac.add(self)
        
        self.rychlost_x = rychlost_hrace_x
        self.rychlost_y = rychlost_hrace_y
        
        self.rychlost_strelby = rychlost_strelby
        self.pocitadlo_strelby = 0
        
    def update(self):
        # ovladani pohybu
        key = pygame.key.get_pressed()
        
        if key[pygame.K_UP]:
            self.rect.y -= self.rychlost_y
        if key[pygame.K_DOWN]:
            self.rect.y += self.rychlost_y
        if key[pygame.K_LEFT]:
            self.rect.x -= self.rychlost_x
        if key[pygame.K_RIGHT]:
            self.rect.x += self.rychlost_x
        
        # omezeni pohybu
        if self.rect.right > velikost_okna_x:
            self.rect.right = velikost_okna_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > velikost_okna_y:
            self.rect.bottom = velikost_okna_y
        if self.rect.top < 0:
            self.rect.top = 0

        # strelba
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
        self.rect.centerx = hrac.rect.centerx
        self.rect.y = hrac.rect.centery - 15
        
        vykreslovaci_skupina_strely.add(self)
        
        self.rychlost = rychlost_strely
        
    def update(self):
        self.rect.y -= self.rychlost
        
        if self.rect.bottom < 0:
            self.kill()

class Nepritel(pygame.sprite.Sprite):
    def __init__(self):
        self.image = textura_nepritel
        
        pygame.sprite.Sprite.__init__(self)
        
        self.rect = self.image.get_rect()
        # nahodne horizontalni umisteni
        self.rect.x = random.randint(0, velikost_okna_x - self.rect.width)
        # zacina tesne nad okrajem okna
        self.rect.y = -self.rect.height
        
        # zabraneni kolizim s dalsimi neprateli
        while pygame.sprite.spritecollide(self, vykreslovaci_skupina_nepratele, False):
            self.rect.x = random.randint(0, velikost_okna_x - self.rect.width)
        
        vykreslovaci_skupina_nepratele.add(self)
                
        self.rychlost = rychlost_nepratel
    
    def update(self):
        self.rect.y += self.rychlost
        
        if self.rect.top > velikost_okna_y:
            self.kill()

# pomocne funkce
def zkontrolovat_vypnuti_hry():
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit()
    
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

def zobrazit_menu():
    okno.fill((255, 255, 255))
    okno.blit(pozadi_menu, (0, 0))
    okno.blit(tlacitko_play, (500, 65))
    okno.blit(tlacitko_credits, (500, 330))
    okno.blit(tlacitko_quit, (500, 595))

def zobrazit_konec_hry():
    okno.blit(pozadi_hra, (0, 0))
    okno.blit(textura_konec_hry, (0, 0))
    
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
            pass # TODO
    elif cursor[0] > 500 and cursor[0] < 1150 and cursor[1] > 615 and cursor[1] < 815:
        okno.blit(tlacitko_quit_vybrano, (500, 595))
        
        if pygame.mouse.get_pressed()[0]:
            exit()

# zacatek programu
vykreslovaci_skupina_hrac = pygame.sprite.Group()
vykreslovaci_skupina_strely = pygame.sprite.Group()
vykreslovaci_skupina_nepratele = pygame.sprite.Group()

hrac = Hrac()

rezim_hry = 'menu'

while rezim_hry == 'menu':
    zkontrolovat_vypnuti_hry()
    
    zobrazit_menu()
    vybrat_z_menu()

    pygame.display.update()

while rezim_hry == 'hra':
    # vypinani
    zkontrolovat_vypnuti_hry()
    
    # generovani nepratel
    if len(vykreslovaci_skupina_nepratele.sprites()) < max_pocet_nepratel:
        Nepritel()
    # sestrelovani nepratel
    pygame.sprite.groupcollide(vykreslovaci_skupina_nepratele, vykreslovaci_skupina_strely, True, True)
    
    # srazka hrace s nepritelem
    if pygame.sprite.groupcollide(vykreslovaci_skupina_hrac, vykreslovaci_skupina_nepratele, False, True):
        zivoty_hrace -= 1
        if zivoty_hrace == 0:
            zobrazit_konec_hry()
    
    # vykresleni
    okno.blit(pozadi_hra, (0, 0))
        
    vykreslovaci_skupina_hrac.update()
    vykreslovaci_skupina_strely.update()
    vykreslovaci_skupina_nepratele.update()
    
    vykreslovaci_skupina_hrac.draw(okno)
    vykreslovaci_skupina_strely.draw(okno)
    vykreslovaci_skupina_nepratele.draw(okno)
    
    pygame.display.update()
