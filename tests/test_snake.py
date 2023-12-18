serpent=[(4,0),(3,0),(2,0),(1,0)] # liste initiale des positions
sh,direct,width,height,tile_size,posp,serpent,fruit,v_gameover_on_exit,v_g=True,"d",20,12,20,(4,0),serpent,(0,0),False,True # paramètres initiaux du jeu 


def test_get_score():
    assert snake.get_score(serpent)==0

def test_move_snake():
    assert move_snake(sh,direct,width,height,tile_size,posp,serpent,fruit,v_gameover_on_exit,v_g)==[(5,0),(4,0),(3,0),(2,0)],(5,0),True # On vérifie si la position du serpent passe bien de (1,0) à 