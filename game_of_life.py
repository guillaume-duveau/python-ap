
def read_args(): # définition des arguments en ligne de commande
    parser = argparse.ArgumentParser(description='Some description.')
    parser.add_argument('-i my_input_file.txt', default='schema_depart.txt',help="position initiale du jeu")
    parser.add_argument('-o my_output_file.txt', default='schema_final.txt',help="position finale du jeu")
    parser.add_argument('-m ', default=20 ,help="nombre d'étapes à jouer")
    parser.add_argument('-d ', default=storetrue,help="affichage ou non du jeu")
    parser.add_argument('-f ', default=10,help="nombre d'images par seconde")
    parser.add_argument('-- width', default=800, help="largeur de l'écran")
    parser.add_argument('-- height', default=600, help="hauteur de l'écran")


class cellule:
    def __init__(self,abscisse,ordonnee,couleur):
            self._abscisse=abscisse
            self._ordonnee=ordonnee
            self._couleur=couleur
    
class ensemble_toutes_cellules:
    def __init__(self):
         self._matrice=[[0 for _ in range(m)] for _ in range(n)]
    

    def couleur_element(self,abscisse,ordonnee):
        return self[ordonnee][abscisse]
    
    def matrice_voisinage(self):
        M=[[0 for _ in range(m)] for _ in range(n)]
        for i in range(n): 
            for j in range(m):
                if i==0:
                    if j==0: # On compte le nombre de cases colorées en noir autour d'une case donnée 
                        M[i][j]=couleur_element(0,1)+couleur_element(1,1)+couleur_element(1,0)
                    if j==m-1:
                        M[i][j]= couleur_element(0,m-2)+couleur_element(1,m-1)+couleur_element(m-2,1)  
                    else:
                        M[i][j]= couleur_element(0,j+1)+couleur_element(0,j-1)+couleur_element(1,j)
                if i==n-1:
                    if j==0:
                        M[i][j]=couleur_element(n-1,0)+couleur_element(n-2,1)+couleur_element(n-1,1)
                    if j==m-1:
                        M[i][j]= couleur_element(n-1,m-2)+couleur_element(n-2,m-2)+couleur_element(n-2,m-1)  
                    else:
                        M[i][j]= couleur_element(n-1,j+1)+couleur_element(n-1,j-1)+couleur_element(n-2,j)

                M[i][j]=couleur_element(i-1,j)+couleur_element(i+1,j)+couleur(i,j-1)+couleur_element(i,j+1)
        return M
    
    def nouvelle_matrice(self):
        matrice_tr=self.matrice_voisinage
        nv_mat=[[0 for _ in range(m)] for _ in range(m)]# On crée une nouvemlle matrice initialement avec des 0
        for i in range(n):
            for j in range(m):
                if couleur_element(self,i,j):
                        # On utilise la connaissance du nombre de cellules noires autour de la cellule considérée
                    if (matrice_tr[i][j] == 2) or (matrice_tr[i][j] == 3) :
                        nv_mat[i][j]=1
                    else:
                        nv_mat[i][j] = 0
                else:
                    if 3 <= matrice_tr[i][j] :
                        nv_mat[i][j] = 1
                    else:
                        nv_mat[i][j] = 0
        return nv_mat

class affichage:
      
    def __init__(self):
        screen=pg.display.set_mode((args.width,args.height)) 
        screen.fill((0,0,0)) # On remplit en blanc l'écran
        


def mise_a_jour_jeu(nv_mat): # l'argument est la "matrice binaire"
    for k in range(0,width,tile_size): # on itère d'abord sur la largeur du damier
        for j in range(0,height,2*tile_size): # puis sur sa profondeur
            if  nv_mat[i][j]:
                pg.draw.rect(screen,(255,255,255),(k,j,tile_size,tile_size)) # On colorie en noir si la matrice indique "1"
    pg.display.update()



if  args.d:  # On initialise l'écran seulement si cela a été demandé     
    pg.init()

    
def main():

    matri=ensemble_toutes_cellules([[0 for _ in range(m)] for _ in range(n)])
    if  args.d:  # On initialise l'écran seulement si cela a été demandé     
        pg.init()
        affichage.__init__()

    for i in range(args.m):
        matri=matri.nouvelle_matrice.copy()


        if args.d:
            pg.time.delay(int(1000/args.f)) # On impose un retard donné pour commander le nombre d'affichages


    if args.d:
        pg.quit()