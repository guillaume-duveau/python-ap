import align 
import pytest

def test_trouver_score():
    assert align.trouver_score("","",-2,1,-1)
    assert align.trouver_score("A","A",-2,1,-1)

L=['AAA','AA-','BACT','BA--','AAAA','AAAA']

def test_meilleur_alignement():
    assert align.meilleur_alignement(L)==4,'AAAA','AAAA'

def test_traitement():
    