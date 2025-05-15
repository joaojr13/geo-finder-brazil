import queue
from services.fabrica_workers import criar_processos_regiao
from multiprocessing import Queue


class BuscaFacade:
    def __init__(self, estrategia):
        self.estrategia = estrategia

    def buscar(self, nome_cidade, estado):
        resultado_queue = Queue()

        processos = criar_processos_regiao(
            cidade_busca=nome_cidade,
            estado_busca=estado,
            estrategia=self.estrategia,
            resultado_queue=resultado_queue
        )

        for p in processos:
            p.start()

        resultados = []
        try:
            while True:
                resultado = resultado_queue.get(timeout=10)
                resultados.append(resultado)
        except queue.Empty:
            pass

        for p in processos:
            p.join()

        return resultados
