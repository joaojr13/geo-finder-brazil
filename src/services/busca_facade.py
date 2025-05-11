import queue
from services.fabrica_workers import criar_processos_regiao
from services.observador_encerramento import ObservadorEncerramento
from multiprocessing import Queue


class BuscaFacade:
    def __init__(self, estrategia):
        self.estrategia = estrategia
        self.observador = ObservadorEncerramento()

    def buscar(self, nome_cidade, estado):
        resultado_queue = Queue()
        # observador = ObservadorEncerramento()  # NOVO: criar um novo a cada chamada

        processos = criar_processos_regiao(
            cidade_busca=nome_cidade,
            estado_busca=estado,
            estrategia=self.estrategia,
            resultado_queue=resultado_queue,
            observador=None
        )

        for p in processos:
            p.start()

        resultados = []
        try:
            while True:
                resultado = resultado_queue.get(timeout=1)
                resultados.append(resultado)
        except queue.Empty:
            pass

        # observador.notificar_encerramento()

        for p in processos:
            p.join()

        return resultados
