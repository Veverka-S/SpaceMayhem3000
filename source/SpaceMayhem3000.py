# pouzite baliky/knihovny
import sys
import random
import pygame as pg

# parametry aplikace
velikost_okna_x = 1650
velikost_okna_y = 850

rychlost_hrace_y = 5
rychlost_hrace_x = 7

zivoty_hrace = 3
skore = 0

rychlost_strely = 10
rychlost_strelby = 8

max_pocet_nepratel = 5
rychlost_nepratel = 2

# inicializace
pg.init()
pg.display.set_caption("Markovo Space Mayhem")
okno = pg.display.set_mode((velikost_okna_x, velikost_okna_y))

# herni assety
menu_pozadi = pg.image.load('obrazky/menu_pozadi.jpg')
herni_pozadi = pg.image.load('obrazky/herni_pozadi.jpg')

tlacitko_play = pg.image.load('obrazky/tlacitko_play.jpg')
tlacitko_play_vybrane = pg.image.load('obrazky/tlacitko_play_vybrane.jpg')
tlacitko_credits = pg.image.load('obrazky/tlacitko_credits.jpg')
tlacitko_credits_vybrane = pg.image.load('obrazky/tlacitko_credits_vybrane.jpg')
tlacitko_quit = pg.image.load('obrazky/tlacitko_quit.jpg')
tlacitko_quit_vybrane = pg.image.load('obrazky/tlacitko_quit_vybrane.jpg')
tlacitko_endless_game = pg.image.load('obrazky/tlacitko_endless_game.jpg')

hrac = pg.image.load('obrazky/hrac.png').convert_alpha()
strela = pg.image.load('obrazky/strela.png').convert_alpha()
nepritel = pg.image.load('obrazky/nepritel.png').convert_alpha()
konec_hry = pg.image.load('obrazky/konec_hry.png').convert_alpha()

# pomocne tridy
class Hrac(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = hrac
        
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
        key = pg.key.get_pressed()
        
        if key[pg.K_UP]:
            self.rect.y -= self.rychlost_y
        if key[pg.K_DOWN]:
            self.rect.y += self.rychlost_y
        if key[pg.K_LEFT]:
            self.rect.x -= self.rychlost_x
        if key[pg.K_RIGHT]:
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

        if key[pg.K_SPACE]:
            if self.pocitadlo_strelby > self.rychlost_strelby:
                Strela(self)
                self.pocitadlo_strelby = 0

class Strela(pg.sprite.Sprite):
    def __init__(self, hrac):
        self.image = strela
        
        pg.sprite.Sprite.__init__(self)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = hrac.rect.centerx
        self.rect.y = hrac.rect.centery - 15
        
        vykreslovaci_skupina_strely.add(self)
        
        self.rychlost = rychlost_strely
        
    def update(self):
        self.rect.y -= self.rychlost
        
        if self.rect.bottom < 0:
            self.kill()

class Nepritel(pg.sprite.Sprite):
    def __init__(self):
        self.image = nepritel
        
        pg.sprite.Sprite.__init__(self)
        
        self.rect = self.image.get_rect()
        # nahodne horizontalni umisteni
        self.rect.x = random.randint(0, velikost_okna_x - self.rect.width)
        # zacina tesne nad okrajem okna
        self.rect.y = -self.rect.height
        
        # zabraneni kolizim s dalsimi neprateli
        while pg.sprite.spritecollide(self, vykreslovaci_skupina_nepratele, False):
            self.rect.x = random.randint(0, velikost_okna_x - self.rect.width)
        
        vykreslovaci_skupina_nepratele.add(self)
                
        self.rychlost = rychlost_nepratel
    
    def update(self):
        self.rect.y += self.rychlost
        
        if self.rect.top > velikost_okna_y:
            self.kill()

# pomocne funkce
def zkontrolovat_vypnuti_hry():
    for event in pg.event.get() :
        if event.type == pg.QUIT :
            pg.quit()
            sys.exit()
    
    if pg.key.get_pressed()[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()

def zobrazit_menu():
    okno.fill((255, 255, 255))
    okno.blit(menu_pozadi, (0, 0))
    okno.blit(tlacitko_play, (500, 65))
    okno.blit(tlacitko_credits, (500, 330))
    okno.blit(tlacitko_quit, (500, 595))

def zobrazit_vyber_modu():
    okno.fill((255,255,255))
    okno.blit(menu_pozadi,(0,0))
    okno.blit(tlacitko_endless_game,(500,300))
    

def zobrazit_konec_hry():
    okno.blit(herni_pozadi, (0, 0))
    okno.blit(konec_hry, (0, 0))
    
    font = pg.font.Font(None, 50)
    s = "Final score: " + str(skore)
    text = font.render(s, 1, (255,255,255))
    okno.blit(text,(700,600))
    
    while True:
        zkontrolovat_vypnuti_hry()
        pg.display.update()

def zobrazeni_zivotu():
    if zivoty_hrace == 3:
        font = pg.font.Font(None,25)
        s = "Health: " + str(zivoty_hrace)
        text = font.render(s, 1, (255,255,255))
        okno.blit(text,(0,0))
    elif zivoty_hrace == 2:
        font = pg.font.Font(None,25)
        s = "Health: " + str(zivoty_hrace)
        text = font.render(s, 1, (200,100,0))
        okno.blit(text,(0,0))
    elif zivoty_hrace == 1:
        font = pg.font.Font(None,25)
        s = "Health: " + str(zivoty_hrace)
        text = font.render(s, 1, (255,0,0))
        okno.blit(text,(0,0))
    
def zobrazeni_skore_ve_hre():
    font = pg.font.Font(None, 25)
    s = "Score: " + str(skore)
    text = font.render(s,1,(255,255,255))
    okno.blit(text,(0,25))

def vybrat_z_menu():
    global herni_mod
    
    cursor = pg.mouse.get_pos()
    
    if cursor[0] > 500 and cursor[0] < 1150 and cursor[1] > 65 and cursor[1] < 265:
        okno.blit(tlacitko_play_vybrane, (500, 65))
        
        if pg.mouse.get_pressed()[0]:
            herni_mod = 'vyber_modu'
    elif cursor[0] > 500 and cursor [0] < 1150 and cursor[1]  > 330 and cursor[1] < 550:
        okno.blit(tlacitko_credits_vybrane, (500, 330))
        
        if pg.mouse.get_pressed()[0]:
            pass # TODO
    elif cursor[0] > 500 and cursor[0] < 1150 and cursor[1] > 615 and cursor[1] < 815:
        okno.blit(tlacitko_quit_vybrane, (500, 595))
        
        if pg.mouse.get_pressed()[0]:
            exit()

def vybirani_herniho_modu():
    global herni_mod
    
    cursor = pg.mouse.get_pos()
    
    
    if cursor[0] > 500 and cursor[0] < 1150 and cursor[1] > 300 and cursor[1] < 500:
        if pg.mouse.get_pressed()[0]:
            herni_mod = 'nekonecna_hra'
    
# zacatek programu
vykreslovaci_skupina_hrac = pg.sprite.Group()
vykreslovaci_skupina_strely = pg.sprite.Group()
vykreslovaci_skupina_nepratele = pg.sprite.Group()

hrac = Hrac()

herni_mod = 'menu'

while herni_mod == 'menu':
    zkontrolovat_vypnuti_hry()
    
    zobrazit_menu()
    vybrat_z_menu()

    pg.display.update()

while herni_mod == 'vyber_modu':
    zkontrolovat_vypnuti_hry()
    
    zobrazit_vyber_modu()
    vybirani_herniho_modu()
    
    
    pg.display.update()

while herni_mod == 'nekonecna_hra':
    # vypinani
    zkontrolovat_vypnuti_hry()
    
    # generovani nepratel
    if len(vykreslovaci_skupina_nepratele.sprites()) < max_pocet_nepratel:
        Nepritel()
    # sestrelovani nepratel
    if pg.sprite.groupcollide(vykreslovaci_skupina_nepratele, vykreslovaci_skupina_strely, True, True):
        skore +=  100
    
    # srazka hrace s nepritelem
    if pg.sprite.groupcollide(vykreslovaci_skupina_hrac, vykreslovaci_skupina_nepratele, False, True):
        zivoty_hrace -= 1
        if zivoty_hrace == 0:
            zobrazit_konec_hry()

    
    # vykresleni
    okno.blit(herni_pozadi, (0, 0))
        
    vykreslovaci_skupina_hrac.update()
    vykreslovaci_skupina_strely.update()
    vykreslovaci_skupina_nepratele.update()
    
    vykreslovaci_skupina_hrac.draw(okno)
    vykreslovaci_skupina_strely.draw(okno)
    vykreslovaci_skupina_nepratele.draw(okno)
    
    zobrazeni_zivotu()
    zobrazeni_skore_ve_hre()
    
    pg.display.update()

