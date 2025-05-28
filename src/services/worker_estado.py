import threading
from data.cidades import get_cidades_por_estado, Cidade

class WorkerEstado(threading.Thread):
    def __init__(self, estado, cidade_busca, estado_busca, estrategia, resultado_queue):
        super().__init__()
        self.estado = estado
        self.cidade_busca = cidade_busca
        self.estado_busca = estado_busca
        self.estrategia = estrategia
        self.resultado_queue = resultado_queue

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
                    print(f'Thread {self.estado} encontrou: {cidade.nome}/{cidade.estado}')
                    return
            else:
                if self.estrategia.comparar(cidade.nome, self.cidade_busca):
                    self.resultado_queue.put({
                        "cidade": cidade.nome,
                        "estado": cidade.estado,
                        "coordenadas": (cidade.latitude, cidade.longitude)
                    })
                    print(f'Thread {self.estado} encontrou: {cidade.nome}/{cidade.estado}')
                    return

        print(f'Thread {self.estado} não encontrou nenhuma cidade correspondente - finalizando')
