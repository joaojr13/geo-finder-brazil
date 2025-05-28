from services.fabrica_processos import FabricaProcessosRegiao
from multiprocessing import Queue
class BuscaFacade:
    def __init__(self, estrategia):
        self.estrategia = estrategia

    def buscar(self, nome_cidade, estado):
        resultado_queue = Queue()

        fabrica = FabricaProcessosRegiao(
            cidade_busca=nome_cidade,
            estado_busca=estado,
            estrategia=self.estrategia,
            resultado_queue=resultado_queue
        )

        processos = fabrica.criar_todos()

        for p in processos:
            p.start()

        for p in processos:
            p.join()

        resultados = []

        while not resultado_queue.empty():
            resultados.append(resultado_queue.get())

        return resultados