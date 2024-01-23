# importation des modules utiles 
import pygame as pg
import numpy as np
import argparse
import logging
import sys
import random 
import re
from pathlib import Path

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
    parser.add_argument('--high-scores-file', default='python-ap/scoresmax.txt')
    parser.add_argument('--max-high-scores', default=5)
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

scores_eleves = Path('scoresmax.txt')

def fichier_scores_eleves(): # On vérifie l'existence du fichier des scores 
    if scores_eleves.is_file():
        return True 
    return False 
    
def creer_fichier_scores(nb_score): 
    if not(fichier_scores_eleves()): # Si le fichier n'existe pas, on en crée un nouveau 
        fichier=open("scoresmax.txt","a") 
        L=[]   
        L.append("inconnu"+ " 0") # On suppose qu'aucun score ne dépasse alors 0. 
        for i in range(nb_score-1):
            L.append("\ninconnu "+ "0")
        fichier.writelines(L)

def lire_scores(): #ON TRANSFORME le fichier en dictionnaire des scores faits par les joueurs ( peu pratique et utile)
    d={}
    with open('scoresmax.txt') as f:
        for line in f:
            line=line.rstrip()
            print(line)
            d[line[:len(line)-2]]=int(line[len(line)-1])
    return d
    
def trouver_indi(nv_valeur): # on trouve l'indice d'insertion du nouveau score 
    f = open("scoresmax.txt","r")
    contenu=f.readlines()
    f.close()
    for k in range(len(contenu)): # on récupère les données chiffrées utiles
        contenu[k]=int(re.findall('[0-9]',contenu[k])[0])
    i_r=0
    for i in range(len(contenu)-1):
        if (nv_valeur > int(contenu[i+1])) and (nv_valeur < (1 + int(contenu[i]))):
            i_r=i #on choisit le dernier indice adapté 
    return i_r # Si aucun indice ne convient, c'est que le nouveau score est un  maximum d'où i_r=0

def changer_scores(nv_valeur,nom): # fonction pour changer une valeur dans le fichier 
    indice=trouver_indi(nv_valeur)
    f = open("scoresmax.txt","r")
    contenu=f.readlines()
    contenu_c=contenu.copy()
    contenu_c[indice]=nom+" "+str(nv_valeur)+"\n"
    for i in range(indice+1,len(contenu)):
        contenu_c[i]=contenu[i-1]
    f.close()
    f=open("scoresmax.txt","w")
    f.writelines(contenu_c)
    f.close()

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
    return len(serpent)-4 # On déduit le score directement de la longueur du serpent 

# mise à jour de la position du fruit 
def update_fruit(width,height,tile_size):
    fruit = (random.randint(0,width//tile_size-1),random.randint(0,height//tile_size-1)) # "-1" pour éviter que le fruit ne sorte du cadre de jeu 
    return fruit

# mise à jour de l'affichage 
def update_display(screen,width,height,bg_color_1,bg_color_2,snake_color,fruit_color,tile_size,serpent,fruit):
    draw(screen,width,height,bg_color_1,bg_color_2,snake_color,fruit_color,tile_size,serpent,fruit)
    pg.display.set_caption(f"snake-score:{get_score(serpent)}")
    pg.display.update()

#gestion de la position du serpent  
def move_snake(sh,direct,width,height,tile_size,posp,serpent,fruit,v_gameover_on_exit,v_g): #( posp est la position précédente)
    pos = tuple(map(lambda i,j : i+j , posp ,tuple(dict_direct[direct]))) # fonction ad-hoc "d'addition terme-à-terme" des tuples représentant la position 
    
    if pos in serpent[1:]: # arrêt du jeu si le serpent entre en collision avec lui-même
        if v_g: # affichage en fonction de la valeur de  args.g
            logger.info("Le serpent est entré en collision avec lui-même")
        sh = False 
    
    fruit_mange=False
    if pos == fruit :
        if v_g: # affichage en fonction de la valeur de  args.g
            logger.info('le serpent a mangé un fruit')
            fruit_mange=True # On utilise cette variable pour pouvoir quand même modifier la position du fruit 
        fruit=update_fruit(width,height,tile_size)

    # gestion de la sortie d'écran du serpent
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
    
    if fruit_mange: # on allonge éventuellement (fruit mangé ou non) la liste "serpent" a 
        serpent.append(ajout_serpent) # On ajoute éventuellement la dernière case retirée
        
        
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
    nb_score=args.max_high_scores
    
    creer_fichier_scores(nb_score) # On crée le fichier des scores 

    if v_g: # affichage en fonction de la valeur de  args.g

        logger.setLevel(logging.DEBUG)
    

    # initialisation de l'écran et de l'horloge
    screen=pg.display.set_mode((width,height)) 
    screen.fill(bg_color_1)
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
    if get_score(serpent) >  min(list(lire_scores().values())):
        changer_scores(get_score(serpent),input("Nom du joueur ?"))

    quit(0)

main()