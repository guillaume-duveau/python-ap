# importation des modules 
import pygame as pg

#CONSTANTES 
BLACK,SCREEN_WIDTH,SCREEN_HEIGHT,CLOCK_FREQUENCY=(0,0,0),400,300,5.5
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
_SIZE=20
H=(0,-1)
B=(0,+1)
D=(1,0)
G=(-1,0)
dict_direct={"h":H,"b":B,"d":D,"g":G}

# intialisation
pg.init()
clock=pg.time.Clock()
SCREEN= pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
sh=True

# Caractéristiques du serpent 
pos=(5,10) # colonne ligne 
long_p=3
long=long_p
direct_p="d"
serpent=[tuple(map(lambda i,j : i+j , pos ,tuple(dict_direct[direct_p])))]
for k in range(long):
    serpent.append(tuple(map(lambda i,j : i+j , serpent[-1] ,tuple(dict_direct[direct_p]))))

# caractéristiques du fruit 
fruit=(3,3)
# BOUCLE
while sh:  
    clock.tick(CLOCK_FREQUENCY)
    SCREEN.fill(WHITE)
    for k in range(0,SCREEN_WIDTH,_SIZE):
        if int(k/20)%2:
            for j in range(0,SCREEN_HEIGHT,2*_SIZE):
                pg.draw.rect(SCREEN,BLACK,(k,j,_SIZE,_SIZE))
        else:
            for j in range(20,SCREEN_HEIGHT,2*_SIZE):
                pg.draw.rect(SCREEN,BLACK,(k,j,_SIZE,_SIZE))

# gestion de la direction 
    direct=direct_p # sans changement de direction, le serpent continue tout droit 
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                direct="h"
            elif event.key == pg.K_DOWN:
                direct="b"
            elif event.key == pg.K_RIGHT:
                direct="d"
            elif event.key == pg.K_LEFT:
                direct="g"    
            elif event.key == pg.K_q:
                sh=False
        if event.type == pg.QUIT:
            sh=False

#gestion de l'affichage du fruit 
    pg.draw.rect(SCREEN,RED,(fruit[0]*_SIZE,fruit[1]*_SIZE,_SIZE,_SIZE))


#gestion de la position du serpent 

    pos = tuple(map(lambda i,j : i+j , pos ,tuple(dict_direct[direct])))
    direct_p=direct
    serpent.insert(0,pos)
    ajout_serpent=serpent.pop()# cas que l'on ajoute éventuellement si le serpent s'allonge
    if not (long==long_p):
        serpent.append(ajout_serpent)
    long=long_p
     
#gestion de la position du fruit 
    if pos == fruit :
        if fruit==(3,3):
            fruit=(15,10)
        else:
            fruit=(3,3)
        long+=1

# gestion de l'affichage du serpent 
    for tile in serpent:
        pg.draw.rect(SCREEN,GREEN,(tile[0]*_SIZE,tile[1]*_SIZE,_SIZE,_SIZE))
    pg.display.update()

    
pg.quit()
quit(0)
