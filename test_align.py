import align

def test_fichier_entree(fichier='fichierADN.txt'): # On vérifie que le fichier initial existe bien 
    assert bool(align.lignes_non_vides(fichier))

seq1='ATCG'
seq2='ATCGG'
def test_needlemann_wunsch(): 
    assert align.needlemann_wunsch(seq1, seq2,)==('ATCG-',seq2) # On vérifie que l'on obtient bien la valeur souhaitée 

def test_traitement_needlemann_wunsch():
    assert bool(align.traitement_needlemann_wunsch(seq1,seq2))

def test_trouver_score():
    assert align.trouver_score('ATCG-','ATCGG')==-3

L=['CCGG','ACCG','ATCG','ATCGG']

def test_meilleur_alignement():
    assert align.meilleur_alignement(L)[0]== 3 
