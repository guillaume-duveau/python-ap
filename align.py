import sys
import re 
seq=''
var=''
id_seq=None
id_var=None

i=0
for line in sys.stdin: # On utilise directement le flux d'entrée de la fonction => IL FAUT UNE ENTREE ( du type programme.py < texte.txt)
    line=line.rstrip() # On enlève le "/n " en fin de ligne
    if re.match(";",line):
        continue
    i+=1
    else:
        if re.match('(var)+$',line) and (id_seq):
            line=line[1:]
            var=str(line)
            continue
        elif re.match("(>seq)+$",line):
            seq=linev
            id_seq=True
            continue

def needleman_wunsch(seq1, seq2, match=2, mismatch=-1, gap_penalty=-1):
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

def trouver_score(align_seq1,align_seq2,penalite_gap=-1,score_align):
    for i in range(len(align_seq1)):
        if (align_seq1[i] == '-') or (align_seq2[i] == '-') :
            score+=penalite_gap
        elif align_seq1[i]==align_seq2[i]:
            score+=score_align

    
