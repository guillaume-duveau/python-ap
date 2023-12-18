import sys
import re 


"""lignes_non_vides=[]
for seq in sys.stdin:# on l'utilise pour lire les commandes données par l'utilisateur 
    lignes_non_vides.append(seq)
"""

def lire_fichier_adn(chemin_fichier): # On extrait les lignes du fichierADN
    try:
        with open(chemin_fichier, 'r') as fichier:
            # Lire le contenu du fichier
            contenu = fichier.read()

            # Diviser le contenu en lignes
            lignes = contenu.split('\n')

            # Filtrer les lignes vides
            lignes_non_vides = [ligne.strip() for ligne in lignes if ligne.strip()]

            return lignes_non_vides
    except FileNotFoundError:
        print(f"Le fichier '{chemin_fichier}' n'a pas été trouvé.")
        return []
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return []


def mise_en_forme(lignes_non_vides):#On retire les premières lignes (elles sont inutiles) 
    try:
        L=[]
        passer_var=False
        passer_seq=False
        for i in range(2,len(lignes_non_vides)):
            if passer_var:
                L.append(lignes_non_vides[i])
                passer_var=False
            elif passer_seq:
                L.append(lignes_non_vides[i])
                passer_seq=False        
            elif bool(re.match('(>seq)+',lignes_non_vides[i])):
                passer_seq=True # lors de l'itération suivante on "passe dans le premier elif"
            elif bool(re.match('(>var)+',lignes_non_vides[i])):
                passer_var=True # lors de l'itération suivante on "passe dans le if passer_var"
            else:
                L[-1]=L[-1]+lignes_non_vides[i] # traiter le cas d'une ligne avec un seul caractère
        return L
    except Exception: 
        print("Il y a eu un problème lors de l'itération")

def needlemann_wunsch(seq1, seq2, match=2, mismatch=-1, gap_penalty=-1): # 
    # Initialisation de la matrice de score
    rows, cols = len(seq1) + 1, len(seq2) + 1
    score_matrix = [[0] * cols for _ in range(rows)]

    # Initialisation de la première colonne avec les pénalités de gap
    for i in range(1, rows):
        score_matrix[i][0] = i * gap_penalty

    # Initialisation de la première ligne avec les pénalités de gap
    for j in range(1, cols):
        score_matrix[0][j] = j * gap_penalty

    # Remplissage de la matrice de score en utilisant la formule récursive
    for i in range(1, rows):
        for j in range(1, cols):
            match_score = score_matrix[i - 1][j - 1] + (match if seq1[i - 1] == seq2[j - 1] else mismatch)
            delete_score = score_matrix[i - 1][j] + gap_penalty
            insert_score = score_matrix[i][j - 1] + gap_penalty
            score_matrix[i][j] = max(match_score, delete_score, insert_score)

    # Reconstruction de l'alignement optimal
    align_seq1, align_seq2 = "", ""
    i, j = rows - 1, cols - 1

    while i > 0 or j > 0:
        current_score = score_matrix[i][j]
        diagonal_score = score_matrix[i - 1][j - 1] if i > 0 and j > 0 else float('-inf')
        up_score = score_matrix[i - 1][j] if i > 0 else float('-inf')
        left_score = score_matrix[i][j - 1] if j > 0 else float('-inf')

        if current_score == diagonal_score + (match if seq1[i - 1] == seq2[j - 1] else mismatch):
            align_seq1 = seq1[i - 1] + align_seq1
            align_seq2 = seq2[j - 1] + align_seq2
            i -= 1
            j -= 1
        elif current_score == up_score + gap_penalty:
            align_seq1 = seq1[i - 1] + align_seq1
            align_seq2 = '-' + align_seq2
            i -= 1
        else:
            align_seq1 = '-' + align_seq1
            align_seq2 = seq2[j - 1] + align_seq2
            j -= 1
    return align_seq1, align_seq2

def traitement_needlemann_wunsch(sequences_adn):
    L=[]
    for i in range(len(sequences_adn)//2):
        seq1,seq2=needlemann_wunsch(sequences_adn[2*i],sequences_adn[2*i+1])
        L.append(seq1)
        L.append(seq2)
    return L 

def trouver_score(align_seq1,align_seq2,penalite_gap=-1,score_align=+1,penalite_diff=-2): # On trouve le score pour deux séqueces issues de needle-wunschmann
    score=0
    for i in range(len(align_seq1)):
        if (align_seq1[i] == '-') or (align_seq2[i] == '-') :
            score+=penalite_gap
        elif align_seq1[i]==align_seq2[i]:
            score+=score_align
        else:
            score+=penalite_diff
    return score 

def meilleur_alignement(L): # On cherche le meilleur score et le couple de chaînes qui correspond.
    i_max=0
    max_s=0
    for i in range(len(L)//2):
        if trouver_score(L[2*i],L[2*i+1])>max_s: # On s'intéresse à chaque couple séquence, variant
            max_s=trouver_score(L[2*i],L[2*i+1])
            i_max=i
    return max_s,L[2*i_max],L[2*i_max+1]

# Exemple d'utilisation
chemin_fichier='fichierADN.txt'
lignes_non_vides=lire_fichier_adn(chemin_fichier)
sequences_adn=mise_en_forme(lignes_non_vides)
print(meilleur_alignement(traitement_needlemann_wunsch(sequences_adn)))

# Normalement, l'exercice se fait sur le snake 
#logger=logging.getLogger(__name__)