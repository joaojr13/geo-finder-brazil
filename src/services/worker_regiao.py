# src/services/worker_regiao.py
"""
Worker de região: cria threads por estado e realiza busca local concorrente.
"""
import threading
from data.cidades import get_cidades_por_estado, Cidade

class WorkerEstado(threading.Thread):
    def __init__(self, estado, cidade_busca, estado_busca, estrategia, resultado_queue, observador):
        super().__init__()
        self.estado = estado
        self.cidade_busca = cidade_busca
        self.estado_busca = estado_busca
        self.estrategia = estrategia
        self.resultado_queue = resultado_queue
        self.observador = observador

    def run(self):
        cidades: list[Cidade] = get_cidades_por_estado(self.estado)
        for cidade in cidades:
            if self.estado_busca:
                if cidade.estado == self.estado_busca and self.estrategia.comparar(cidade.nome, self.cidade_busca):
                    self.resultado_queue.put({
                        "cidade": cidade.nome,
                        "estado": cidade.estado,
                        "coordenadas": (cidade.latitude, cidade.longitude)
                    })
                    self.observador.notificar_encerramento()
                    return
            else:
                if self.estrategia.comparar(cidade.nome, self.cidade_busca):
                    self.resultado_queue.put({
                        "cidade": cidade.nome,
                        "estado": cidade.estado,
                        "coordenadas": (cidade.latitude, cidade.longitude)
                    })
                    print(f'Thread {self.estado} encontrou!')
                    return

        print(f'Thread {self.estado} nao encontrou - finalizando!')


def worker_regiao(regiao, estados, cidade_busca, estado_busca, estrategia, resultado_queue, observador):
    threads = []
    for estado in estados:
        thread = WorkerEstado(
            estado=estado,
            cidade_busca=cidade_busca,
            estado_busca=estado_busca,
            estrategia=estrategia,
            resultado_queue=resultado_queue,
            observador=observador
        )
        threads.append(thread)
        thread.start()
        print(f'Processo {regiao} - Thread {estado} criada')

    for thread in threads:
        thread.join()
