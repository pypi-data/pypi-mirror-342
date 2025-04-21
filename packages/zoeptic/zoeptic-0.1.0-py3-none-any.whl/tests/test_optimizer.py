from zoeptic.optimizer import remove_duplicates

def test_remove_duplicates_list():
    assert remove_duplicates([1, 2, 2, 3, 1]) == [1, 2, 3]

def test_remove_duplicates_dict():
    entrada = {'a': 1, 'b': 2, 'c': 1, 'd': 3}
    salida = remove_duplicates(entrada)
    assert salida == {'a': 1, 'b': 2, 'd': 3}

