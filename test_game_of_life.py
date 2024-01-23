def test_fichier_sortie():
    assert game_of_life.read_args().o_my_output_file.is_file()

M=[list('00100000') for _ in range(9)]

def test_bete():
    assert False