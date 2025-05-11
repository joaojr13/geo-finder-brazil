# src/services/observador_encerramento.py
"""
Observer: gerencia o encerramento coordenado de processos e threads.
"""
from multiprocessing import Event


class ObservadorEncerramento:
    def __init__(self):
        self._evento = Event()

    def notificar_encerramento(self):
        self._evento.set()

    def encerrado(self):
        return self._evento.is_set()
