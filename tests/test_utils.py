from src.controllers.utils import eleva_quadrado

def test_eleva_quadrado_sucesso():
    resultado = eleva_quadrado(2)
    resultado == 4