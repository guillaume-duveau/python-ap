import pygame as pg # Importation des modules utiles 
import argparse 
import logging
import sys
import re

BLANC=(255,255,255)
NOIR=(0,0,0)
BLEU=(0,0,255)
TILE_SIZE=20

def read_args(): # définition des arguments en ligne de commande
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-i', default='schema_depart.txt',help="position initiale du jeu")
    parser.add_argument('-o', default='schema_final.txt',help="position finale du jeu")
    parser.add_argument('-m', default=100 ,help="nombre d'étapes à jouer")
    parser.add_argument('-d', action='store_true',help="affichage ou non du jeu")
    parser.add_argument('-f', default=15,help="nombre d'images par seconde")
    parser.add_argument('--width', default=200, help="largeur de l'écran")
    parser.add_argument('--height', default=300, help="hauteur de l'écran")
    parser.add_argument('--tile_size', default=TILE_SIZE, help="hauteur de l'écran")
    
    args = parser.parse_args()

    if int(args.height)%int(args.tile_size) or int(args.width)%int(args.tile_size) : # Il faut que la divisibilité soit assurée 
        raise ValueError("Problème de compatiblité entre la largeur, la longueur et la dimension des cases ")

    return args

# Définition du "root logger" 
logger = logging.getLogger(__name__)
root = logging.getLogger()
handler = logging.StreamHandler(sys.stderr)
fmt = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(fmt)
root.addHandler(handler)
logger.setLevel(logging.DEBUG)

class ensemble_toutes_cellules: # On crée une classe qui permet de "regrouper toutes les cellules" dans le même objet 
    
    def __init__(self,matrice):
        self._matrice=matrice

    def __iter__(self):
        return iter(self)
    
    @staticmethod
    def couleur_element(ensemble,ordonnee,abscisse):
        return int(ensemble._matrice[ordonnee][abscisse])

    def liste_indices(position):# On calcule les indices des éléments voisins d'un point d'indice donné
        L=[(position[0]+1,position[1]),(position[0]-1,position[1]),(position[0],position[1]-1),(position[0],position[1]+1),]
        L.append((position[0]-1,position[1]-1))
        L.append((position[0]-1,position[1]+1))
        L.append((position[0]+1,position[1]+1))
        L.append((position[0]+1,position[1]-1))
        return L 

    def matrice_voisinage(ensemble):# On crée la matrice qui compte le nombre de points colorés autour de chaque point
        largeur=len(ensemble._matrice[0])
        hauteur=len(ensemble._matrice)
        M=[[0 for _ in range(largeur)] for _ in range(hauteur)]
        for i in range(hauteur):
            for j in range(largeur):
                S=0
                for indice in ensemble_toutes_cellules.liste_indices((i,j)): # On somme sur les indices des points voisins
                    if (indice[0] not in range(hauteur)) or (indice[1] not in range(largeur)):
                        S+=0
                    else:
                        S+=ensemble_toutes_cellules.couleur_element(ensemble,indice[0],indice[1])
                M[i][j]=S
        return M
        
    def _nouvelle_matrice(ensemble): # On crée le nouvel ensemble de cases, après une itération complète
        largeur=len(ensemble._matrice[0])
        hauteur=len(ensemble._matrice)
        matrice_tr=ensemble_toutes_cellules.matrice_voisinage(ensemble)
        nv_mat=[[0 for _ in range(largeur)] for _ in range(hauteur)]# On crée une nouvemlle matrice initialement avec des 0
        for i in range(hauteur):
            for j in range(largeur):
                if ensemble_toutes_cellules.couleur_element(ensemble,i,j):
                        # On utilise la connaissance du nombre de cellules noires autour de la cellule considérée pour décider de la couleur de la case suivante
                    if (matrice_tr[i][j] == 2) or (matrice_tr[i][j] == 3) : # ATTENTION matrice_tr est bien une liste de listes, pas un "ensemble_toutes_cellules"
                        nv_mat[i][j] = 1
                    else:
                        nv_mat[i][j] = 0
                else:  # Dans le cas où la cellule est initialement blanche 
                    if  matrice_tr[i][j] == 3:
                        nv_mat[i][j] = 1
                    else:
                        nv_mat[i][j] = 0
        return ensemble_toutes_cellules(nv_mat)

def lire_schema(fi=read_args().i): #ON TRANSFORME le fichier en dictionnaire des scores faits par les joueurs ( peu pratique et utile)
    #ensemble=[[0 for _ in range(read_args().width//read_args().tile_size) ] for _ in range(read_args().height//read_args().tile_size) ]
    with open(fi) as f:
        i=0
        ensemble=[]
        for line in f:
            line=line.rstrip()
            ensemble.append([ 0 for _ in range(max(len(line),read_args().width//read_args().tile_size))])
            for j in range(len(line)):
                ensemble[i][j]=int(line[j])
            i+=1
        if (  read_args().height//read_args().tile_size <= i ):
            return ensemble
        elif (i< int(read_args().height//read_args().tile_size) ):
            for _ in range(int(read_args().height //read_args().tile_size) - i):
                ensemble.append([ 0 for _ in range(max(len(line),read_args().width//read_args().tile_size))])
            return ensemble 
    
def mise_a_jour_jeu(screen,matri,matrip): # l'argument est la "matrice binaire"
    screen.fill(BLANC)
    for j in range(0,len(matri._matrice)): #sur sa hauteur
        for k in range(0,len(matri._matrice[0])): # on itère ensuite  sur la largeur du damier
            if  (matri._matrice[j][k]==1) :
                pg.draw.rect(screen,NOIR,(j*read_args().tile_size,k*read_args().tile_size,read_args().tile_size,read_args().tile_size)) # On colorie en noir si la matrice indique "1"
            pg.display.update()

def verif_fichier_sortie(fichier=read_args().o):
    refaire=False
    f = open(fichier,"r")
    contenu=f.readlines()
    if not(len(contenu)==read_args().height//read_args().tile_size): # SI la
        refaire=True
    elif not((len(contenu[0])==read_args().width//read_args().tile_size)):
        refaire=True
    return refaire 

def refaire_fichier_sortie(ensemble,fichier=read_args().o): # On crée un nouveau fichier texte de sortie
        fichier=open(fichier,"a") 
        L=[]
        for i in range(len(ensemble._matrice)):# Sur la hauteur 
            for j in range(len(ensemble._matrice[0])):# Sur la largeur
                L.append(str(ensemble._matrice[i][j]))
            L.append("\n")
        fichier.writelines(L)
        fichier.close()
        return None 

def changer_fichier_sortie(ensemble,fichier=read_args().o): # 
    L=[]
    fichier=open(fichier,"w")
    for i in range(len(ensemble._matrice)):# Sur la hauteur 
        for j in range(len(ensemble._matrice[0])): # Sur la largeur 
            L.append(str(ensemble_toutes_cellules.couleur_element(ensemble,i,j)))
        L.append("\n")
    fichier.writelines(L)
    fichier.close()
    return None

def main():
    args=read_args()
    matrip=ensemble_toutes_cellules(lire_schema()) # On gard en mémoire l'état précédent du système 
    
    if args.d:  # On initialise l'écran seulement si cela a été demandé 
        pg.init()
        screen=pg.display.set_mode((read_args().width,read_args().height)) 
        screen.fill(BLANC) # On remplit en blanc l'écran
    
    for _ in range(int(read_args().m)):
        matri=ensemble_toutes_cellules._nouvelle_matrice(matrip) # Une itération du jeu 
        if args.d:
            mise_a_jour_jeu(screen,matri,matrip)
            pg.time.delay(int(1000/float(args.f))) # On impose un retard donné pour commander le nombre d'affichages
        
        matrip=matri

    if args.d:
        pg.quit()

    if verif_fichier_sortie():
        refaire_fichier_sortie(matri)
    changer_fichier_sortie(matri)
    return None 

if __name__=="__main__":
    main()