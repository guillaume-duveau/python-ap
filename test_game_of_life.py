import sys    
sys.path.append("C:\Users\alexis\Documents\école\première année\UE 12\Tp 7_11_23\python-ap\game_of_life.py")
import game_of_life

def test_schema_present():  # On vérifie la présence d'un fichier en entrée
    assert game_of_life.lire_schema()

L=[[0] for _ in range(5)] # On construit une matrice de passage que l'on souhaite simple
L[0][1]=1
L[1][0]=1
L[1][1]=1
matri=game_of_life.ensemble_toutes_cellules(L)

L_tr=L.copy() # On construit la matrice de passage d'une matrice à une autre
L_tr[0][0]=3
L_tr[0][1]=2
L_tr[1][1]=2
L_tr[1][0]=2

L_res=L.copy() # On construit la matrice que l'on doit obtenir après une itération
L_res[0][0]=1

def test_matrice_matrice_voisinage():
    assert (game_of_life._matrice_voisinage(matri) == L_tr )

def test_nouvelle_matrice():
    assert (game_of_life._nouvelle_matrice(L)==game_of_life.ensemble_toutes_cellules(L_res))