
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
                    if j==0:
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

                

class affichage:
      
    def __init__(self):
        
     
     