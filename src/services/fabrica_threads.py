from services.worker_estado import WorkerEstado

class FabricaThreadsEstado:
    def __init__(self, regiao, estados, cidade_busca, estado_busca, estrategia, resultado_queue):
        self.regiao = regiao
        self.estados = estados
        self.cidade_busca = cidade_busca
        self.estado_busca = estado_busca
        self.estrategia = estrategia
        self.resultado_queue = resultado_queue

    def criar(self, estado):
        return WorkerEstado(
            estado=estado,
            cidade_busca=self.cidade_busca,
            estado_busca=self.estado_busca,
            estrategia=self.estrategia,
            resultado_queue=self.resultado_queue
        )

    def __call__(self):
        threads = []
        for estado in self.estados:
            thread = self.criar(estado)
            threads.append(thread)
            thread.start()
            print(f'Processo {self.regiao} - Thread {estado} criada')

        for thread in threads:
            thread.join()
        print(f'Processo {self.regiao} finalizado')
