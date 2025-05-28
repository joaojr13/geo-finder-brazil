from multiprocessing import Process
from services.fabrica_threads import FabricaThreadsEstado

REGIOES = {
    "N": {"AC", "AM", "AP", "PA", "RO", "RR", "TO"},
    "NE": {"AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"},
    "CO": {"DF", "GO", "MT", "MS"},
    "SE": {"ES", "MG", "RJ", "SP"},
    "S": {"PR", "RS", "SC"},
}

class FabricaProcessosRegiao:
    def __init__(self, cidade_busca, estado_busca, estrategia, resultado_queue):
        self.cidade_busca = cidade_busca
        self.estado_busca = estado_busca
        self.estrategia = estrategia
        self.resultado_queue = resultado_queue

    def criar_todos(self):
        processos = []
        for regiao, estados in REGIOES.items():
            fabrica_threads = FabricaThreadsEstado(
                regiao=regiao,
                estados=estados,
                cidade_busca=self.cidade_busca,
                estado_busca=self.estado_busca,
                estrategia=self.estrategia,
                resultado_queue=self.resultado_queue
            )
            processo = Process(target=fabrica_threads)  # direto!
            processos.append(processo)
            print(f'Processo {regiao} criado')
        return processos
