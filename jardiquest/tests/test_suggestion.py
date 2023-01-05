from jardiquest.controller import *
from jardiquest.model.database.entity.recolte import Recolte
import uuid
from datetime import datetime

def test_glouton_suggestion_empty():
    assert glouton_solution([],100) == []

def test_glouton_suggestion_zero():
    recoltes = [Recolte(idRecolte=uuid.uuid1(),quantity=5,qtt_recommandee=1),Recolte(idRecolte=uuid.uuid1())]
    assert glouton_solution(recoltes,0) == []

def test_tri_loop():
    tab = [[6],[6],[6],[6],[6],[5],[5],[5],[5],[1],[2],[2],[2],[3],[3],[1],[1],[4],[4],[7]]
    res = [[6],[5],[1],[2],[3],[4],[7],[6],[5],[2],[3],[1],[4],[6],[5],[2],[1],[6],[5],[6]]
    assert triLoop(tab,[]) == res

def test_creation_lots_none():
    recoltes = [Recolte(idRecolte=uuid.uuid1()),Recolte(idRecolte=uuid.uuid1())]
    assert creation_lots(recoltes) == []

def test_tri_bulle():
    tab = [[0,6],[0,6],[0,5],[0,5],[0,5],[0,1],[0,2],[0,7]]
    tri_bulle(tab)
    res = [[0,1],[0,2],[0,5],[0,5],[0,5],[0,6],[0,6],[0,7]]
    assert tab == res

def test_prix_pannier_empty():
    assert prixPanier([]) == 0

def test_creation_dictionnaire_empty():
    assert creation_dictionnaire([]) == {}

def test_suggestion():
    recoltes = [
        Recolte(idRecolte='1',quantity=5,qtt_recommandee=1,cost=2,idCatalogue=1),
        Recolte(idRecolte='2',quantity=4,qtt_recommandee=2,cost=3,idCatalogue=2)
        ]
    res = [[1, 2, 1, '1'], [2, 6, 2, '2'], [1, 2, 1, '1']]
    assert glouton_solution(recoltes,12) == res

def test_creation_dictionnaire():
    tab = [[1, 2, 1, '1'], [2, 6, 2, '2'], [1, 2, 1, '1']]
    assert creation_dictionnaire(tab) == {'1': [2, [1, 2, 1, '1']], '2': [1, [2, 6, 2, '2']]}