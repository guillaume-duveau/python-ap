# importation des modules utiles 
import pygame as pg
import numpy as np
import argparse
import logging
import sys
import random 

#CONSTANTES 
BLACK,WIDTH,HEIGHT,FPS=(0,0,0),400,300,1
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

# Définition du "root logger" 
logger = logging.getLogger(__name__)
root = logging.getLogger()
handler = logging.StreamHandler(sys.stderr)
fmt = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(fmt)
root.addHandler(handler)

def read_args(): # fonction qui renvoie l'ensemble des arguments 
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
    parser.add_argument('-g', help ='log level', action="store_false")
    args = parser.parse_args()
    
    # vérification des arguments
    if (args.bg_color_1 ==  args.bg_color_2) or (args.bg_color_1 ==  args.snake_color) or (args.bg_color_2 ==  args.snake_color):
        raise ValueError("Les couleurs doivent être diférentes") # on vérifie que les couleurs sont différentes

    if (args.bg_color_1 ==  args.fruit_color) or (args.bg_color_2 ==  args.fruit_color) or (args.snake_color ==  args.fruit_color):
        raise ValueError("Les couleurs doivent être diférentes") # même chose mais pour la couleur du fruit 

    if (args.height % args.tile_size) or (args.width % args.tile_size) or (args.width // args.tile_size < 20 ) or (args.height // args.tile_size < 12 ): 
        raise ValueError("Porblème de compatibilité des tailles ")
    
    if args.snake_length < 2:
        raise ValueError("le serpent est trop court")
    return args 

 # fonction qui dessine le damier 
def draw_checkboard(screen,width,height,bg_color_1,bg_color_2,tile_size):
    for k in range(0,width,tile_size): # on itère d'abord sur la largeur du damier
        if int(k/20)%2:
            for j in range(0,height,2*tile_size): # puis sur sa profondeur
                pg.draw.rect(screen,bg_color_2,(k,j,tile_size,tile_size))
        else:
            for j in range(20,height,2*tile_size):
                pg.draw.rect(screen,bg_color_2,(k,j,tile_size,tile_size))
    pg.display.update()

#gestion de l'affichage du fruit 
def draw_fruit(screen,fruit,tile_size,fruit_color=RED):
    pg.draw.rect(screen,fruit_color,(fruit[0]*tile_size,fruit[1]*tile_size,tile_size,tile_size))
    pg.display.update()

# gestion de l'affichage du serpent 
def draw_snake(screen,serpent,snake_color,tile_size):
    for tile in serpent:
        pg.draw.rect(screen,snake_color,(tile[0]*tile_size,tile[1]*tile_size,tile_size,tile_size))
    pg.display.update()

# on définit une fonction qui dessine tout 
def draw(screen,width,height,bg_color_1,bg_color_2,snake_color,fruit_color,tile_size,serpent,fruit):
    screen.fill(bg_color_1)
    draw_checkboard(screen,width,height,bg_color_1,bg_color_2,tile_size)
    draw_snake(screen,serpent,snake_color,tile_size)
    draw_fruit(screen,fruit,tile_size,fruit_color)
    pg.display.update()
 
# fonction qui permet d'obtenir le score actuel du joueur
def get_score(serpent):
    return len(serpent)-3 # On déduit le score directement de la longueur du serpent 

# mise à jour de la position du fruit 
def update_fruit(width,height,tile_size):
    fruit = (random.randint(0,width//tile_size-1),random.randint(0,height//tile_size-1)) # "-1" pour éviter que le fruit ne sorte du cadre de jeu 
    return fruit

# mise à jour de l'affichage 
def update_display(screen,width,height,bg_color_1,bg_color_2,snake_color,fruit_color,tile_size,serpent,fruit):
    draw(screen,width,height,bg_color_1,bg_color_2,snake_color,fruit_color,tile_size,serpent,fruit)
    pg.display.set_caption(f"snake-score:{get_score(serpent)} and pos : {serpent[0]}")
    pg.display.update()

#gestion de la position du serpent  
def move_snake(sh,direct,width,height,tile_size,posp,serpent,fruit,v_gameover_on_exit,v_g): #( posp est la position précédente)
    pos = tuple(map(lambda i,j : i+j , posp ,tuple(dict_direct[direct]))) # fonction ad-hoc "d'addition terme-à-terme" des tuples représentant la position 
    
    if pos in serpent[1:]: # arrêt du jeu si le serpent entre en collision avec lui-même
        if v_g: # affichage en fonction de la valeur de  args.g
            logger.info("Le serpent est entré en collision avec lui-même")
        sh = False 
    
    if v_gameover_on_exit : 
        if pos[0] in [ 0, width // tile_size] or pos[1] in [ 0, height // tile_size ]:
            sh=False # dans ce cas, on arrête le jeu 
    elif not (v_gameover_on_exit): 
        
        if (pos[0] == 0) and (direct == "g"): 
            pos = tuple(np.array([width//tile_size, pos[1] ])) # si le serpent touche le bord de gauche, il part à droite
        if (pos[0] == width//tile_size) and (direct == "d"):
            pos = tuple(np.array([0, pos[1]])) #si le serpent touche le bord de droite, il part à gauche
        if (pos[1] == height//tile_size) and (direct == "b"):
            pos = tuple(np.array([pos[0],0])) # si le serpent touche le bord du bas, il part en haut 
        if (pos[1] == 0) and (direct == "h"): 
            pos =tuple(np.array([pos[0],height//tile_size] ))# si le serpent touche le bord du haut, il part en haut 
    
    serpent.insert(0,pos) # on "ajoute une nouvelle case" au serpent
    ajout_serpent=serpent.pop() # on enlève la dernière case du serpent sauf si on atteint un fruit
    
    if pos == fruit :
        if v_g: # affichage en fonction de la valeur de  args.g
            logger.info('le serpent a mangé un fruit')
        serpent.append(ajout_serpent) # case que l'on ajoute éventuellement si le serpent s'allonge
        fruit=update_fruit(width,height,tile_size)
     # gestion de la sortie d'écran du serpent 
    
    return serpent,fruit,sh

def process_events(sh,screen,width,height,bg_color_1,bg_color_2,snake_color,fruit_color,tile_size,serpent,fruit,v_gameover_on_exit,v_g,direct,pos):
    # gestion de la direction  du serpent 
    # sans changement de direction, le serpent continue tout droit 
    pos=serpent[0]
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

    serpent,fruit,sh=move_snake(sh,direct,width,height,tile_size,pos,serpent,fruit,v_gameover_on_exit,v_g)
    update_display(screen,width,height,bg_color_1,bg_color_2,snake_color,fruit_color,tile_size,serpent,fruit)
    
    return sh,serpent,fruit,direct

    
def main():

    args=read_args()# On lit les arguments du programme 
    
    # on récupère les arguments utiles pour le programme 
    width=args.width # on les renomme afin d'avoir le même nom que ceux des fonctions 
    height=args.height
    bg_color_1=args.bg_color_1
    bg_color_2=args.bg_color_2
    fruit_color=args.fruit_color
    snake_color=args.snake_color
    snake_length=args.snake_length
    tile_size=args.tile_size
    v_gameover_on_exit=args.gameover_on_exit
    v_g=args.g

    if v_g: # affichage en fonction de la valeur de  args.g

        logger.setLevel(logging.DEBUG)
        logger.critical("Il s'est passé quelque chose de grave") # messages d'erreurs différenciés en fonction des incidents
        logger.error("Quelque chose de mal a eu lieu") # message spécifique pour l'erreur 
        logger.warning("Quelque chose s'est mal passé") # message spécifique pour l'avertissement 
    

    # initialisation de l'écran et de l'horloge
    screen=pg.display.set_mode((width,height)) 
    screen.fill(bg_color_1)
    
    score=0 # intialisation de l'affichage du jeu 
    fruit=(3,3) # position initiale du fruit
    pos=(5,10) # colonne, ligne  du serpent 
    direct="d"
    serpent=[tuple(map(lambda i,j : i+j , pos ,tuple(dict_direct["d"])))]
    for k in range(snake_length):
        serpent.append(tuple(map(lambda i,j : i-j , serpent[-1] ,tuple(dict_direct["d"]))))
#===========================================================================================#
    if v_g: # affichage en fonction de la valeur de  args.g
        logger.info("début de la boucle principale")
    sh=True # On initialise la variable à "True" 
    pg.init()
    
    # BOUCLE PRINCIPALE 
    while sh:  
        pg.time.delay(int(1000/args.fps))
        sh,serpent,fruit,direct=process_events(sh,screen,width,height,bg_color_1,bg_color_2,snake_color,fruit_color,tile_size,serpent,fruit,v_gameover_on_exit,v_g,direct,pos)
    pg.quit()
    if args.g: # affichage en fonction de la valeur de  args.g
        logger.info ("fin du jeu")
    quit(0)

main()