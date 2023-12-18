serpent=[(4,0),(3,0),(2,0),(1,0)]
sh,direct,width,height,tile_size,posp,serpent,fruit,v_gameover_on_exit,v_g=True,"d",20,12,20,(4,0),serpent,(5,0),False,True


def test_fruit():
    assert snake.move_snake(sh,direct,width,height,tile_size,posp,serpent,fruit,v_gameover_on_exit,v_g)[0]==[(5,0),(4,0),(3,0),(2,0),(1,0)]
    assert snake.move_snake(sh,direct,width,height,tile_size,posp,serpent,fruit,v_gameover_on_exit,v_g)[2]==True