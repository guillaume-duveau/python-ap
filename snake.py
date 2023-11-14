# importation des modules 
import pygame as pg
import argparse

#CONSTANTES 
BLACK,WIDTH,HEIGHT,FPS=(0,0,0),400,300,6
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
TILE_SIZE=20
LONG_0=3
H=(0,-1)
B=(0,+1)
D=(1,0)
G=(-1,0)
dict_direct={"h":H,"b":B,"d":D,"g":G}

#définiton des arguments de la fonction 
parser = argparse.ArgumentParser(description='Some description.')
parser.add_argument('--bg-color-1', default=WHITE,help="first color of the background checkerboard")
parser.add_argument('--bg-color-2', default=BLACK,help="second color of the background checkerboard")
parser.add_argument('-height', type=int, default=HEIGHT, help="height of the window")
parser.add_argument('-width', type=int, default=WIDTH, help="height of the window")
parser.add_argument('--fps', type=int, default=FPS, help="number of frames per second")
parser.add_argument('--fruit-color', default=RED,help="color of the fruit")
parser.add_argument('--snake-color', default=GREEN,help="color of the snake")
parser.add_argument('--snake-length',type=int, default=LONG_0,  help="length of the snake")
parser.add_argument('--tile-size', type=int, default=TILE_SIZE, help="size of a tail size")
parser.add_argument('--gameover-on-exit', help='A flag.', action='store_true') # on choisit le "mode de jeu"
args = parser.parse_args()
print(args)

# vérification des arguments
if (args.bg_color_1 ==  args.bg_color_2) or (args.bg_color_1 ==  args.snake_color) or (args.bg_color_2 ==  args.snake_color):
    raise ValueError("Les couleurs doivent être diférentes") # on vérifie que les couleurs sont différentes

if (args.bg_color_1 ==  args.fruit_color) or (args.bg_color_2 ==  args.fruit_color) or (args.snake_color ==  args.fruit_color):
    raise ValueError("Les couleurs doivent être diférentes") # même chose mais pour la couleur du fruit 


if (args.height % args.tile_size) or (args.width % args.tile_size) or (args.width // args.tile_size < 20 ) or (args.height // args.tile_size < 12 ): 
    raise ValueError("Porblème de compatibilité des tailles ")
 
if args.snake_length < 2:
    raise ValueError("le serpent est trop court")


# intialisation de l'affichage du jeu 
pg.init()
clock=pg.time.Clock()
SCREEN= pg.display.set_mode((args.width,args.height))
sh=True
score=0

# caractéristiques du fruit 
fruit=(3,3)

# Caractéristiques du serpent 
pos=(5,10) # colonne, ligne 
long_p=LONG_0
long=args.snake_length # long est la longueur actuelle et long_p la longueur précédente
direct_p="d"
serpent=[tuple(map(lambda i,j : i+j , pos ,tuple(dict_direct[direct_p])))]
for k in range(long):
    serpent.append(tuple(map(lambda i,j : i+j , serpent[-1] ,tuple(dict_direct[direct_p]))))

# BOUCLE
while sh:  
    clock.tick(args.fps)
    SCREEN.fill(args.bg_color_1)
    for k in range(0,args.width,args.tile_size):
        if int(k/20)%2:
            for j in range(0,args.height,2*args.tile_size):
                pg.draw.rect(SCREEN,args.bg_color_2,(k,j,args.tile_size,args.tile_size))
        else:
            for j in range(20,args.height,2*args.tile_size):
                pg.draw.rect(SCREEN,args.bg_color_2,(k,j,args.tile_size,args.tile_size))

# gestion de la direction  du serpent 
    direct=direct_p # sans changement de direction, le serpent continue tout droit 
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP: # aller en haut 
                direct="h"
            elif event.key == pg.K_DOWN: # aller en bas 
                direct="b"
            elif event.key == pg.K_RIGHT: # aller à droite
                direct="d"
            elif event.key == pg.K_LEFT: # aller à gauche 
                direct="g"    
            elif event.key == pg.K_q: # presser la touche q 
                sh=False
        if event.type == pg.QUIT:
            sh=False
    
#gestion de l'affichage du fruit 
    pg.draw.rect(SCREEN,RED,(fruit[0]*args.tile_size,fruit[1]*args.tile_size,args.tile_size,args.tile_size))

#gestion de la position du serpent  
    
    pos = tuple(map(lambda i,j : i+j , pos ,tuple(dict_direct[direct])))
    direct_p=direct
    serpent.insert(0,pos) # on "ajoute une nouvelle case" au serpent
    ajout_serpent=serpent.pop() # on enlève la dernière case du serpent sauf si on atteint un fruit
    if pos == fruit :
        serpent.append(ajout_serpent) # case que l'on ajoute éventuellement si le serpent s'allonge
        score+=1
        if fruit==(3,3):
            fruit=(15,10)
        else:
            fruit=(3,3)
        
    # gestion de la sortie de l'écran du serpent 
    if args.gameover_on_exit : 
        if pos[0] in [ 0, args.width // args.tile_size] or pos[1] in [ 0, args.height // args.tile_size ]:
            pg.quit()
    elif not ( args.gameover_on_exit): 
        if (pos[0] == 0) and (direct == "g"): 
            posc = pos
            pos = ( args.width//args.tile_size, posc[1] ) # si le serpent touche le bord de gauche, il part à droite
        if (pos[0] == args.width//args.tile_size) and (direct == "d"):
            posc= pos
            pos = (0, posc[1]) #si le serpent touche le bord de droite, il part à gauche
        if (pos[1] == args.height//args.tile_size) and (direct == "b"):
            posc = pos
            pos = (posc[0],0) # si le serpent touche le bord du bas, il part en haut 
        if (pos[1] == 0) and (direct == "h"):
            posc = pos 
            pos = (posc[0],args.height//args.tile_size )# si le serpent touche le bord du haut  , il part en haut 

    
# gestion de l'affichage du serpent 
    for tile in serpent:
        pg.draw.rect(SCREEN,args.snake_color,(tile[0]*args.tile_size, tile[1]*args.tile_size ,args.tile_size ,args.tile_size))
    pg.display.update()

# gestion de l'affichage du score 
    pg.display.set_caption(f"snake-score:{score}")
pg.quit()
quit(0)