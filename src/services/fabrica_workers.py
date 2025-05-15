from services.worker_regiao import worker_regiao
from multiprocessing import Process
"""
Factory: cria processos para cada região com workers por estado.
"""

# Dicionário com a divisão regional por estados
REGIOES = {
    "N": {"AC", "AM", "AP", "PA", "RO", "RR", "TO"},
    "NE": {"AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"},
    "CO": {"DF", "GO", "MT", "MS"},
    "SE": {"ES", "MG", "RJ", "SP"},
    "S": {"PR", "RS", "SC"},
}


def criar_processos_regiao(cidade_busca, estado_busca, estrategia, resultado_queue):
    processos = []
    for regiao, estados in REGIOES.items():
        processo = Process(
            target=worker_regiao,
            args=(regiao, estados, cidade_busca, estado_busca,
                  estrategia, resultado_queue)
        )
        processos.append(processo)
        print(f'Processo {regiao} criado')
    return processos
