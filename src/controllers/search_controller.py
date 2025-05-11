from data.cidades import load_cidades
from services.busca_facade import BuscaFacade
from services.estrategia_comparacao import ComparacaoFuzzy

facade = BuscaFacade(estrategia=ComparacaoFuzzy())


def buscar_coordenadas(nome_cidade, estado):
    if not nome_cidade:
        return {"erro": "Cidade não informada."}

    # Apenas um estado → buscar coordenadas com a Facade
    resultado = facade.buscar(nome_cidade, estado)

    return resultado
