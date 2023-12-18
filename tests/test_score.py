

serpent=[(4,0),(3,0),(2,0),(1,0)] # liste initiale des positions
sh,direct,width,height,tile_size,posp,serpent,fruit,v_gameover_on_exit,v_g=True,"d",20,12,20,(4,0),serpent,(0,0),False,True # paramètres initiaux du jeu 


def test_get_score():
    assert snake.get_score(serpent)==0

def test_score():
    sh,direct,width,height,tile_size,posp,serpent,fruit,v_gameover_on_exit,v_g=True,"d",20,12,20,(4,0),serpent,(5,0),False,True
    snake.main() # On veut le programme crée un fichier des scores s'il n'existe pas
    assert snake.fichier_scores_eleves


