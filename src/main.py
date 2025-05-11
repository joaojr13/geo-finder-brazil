
from PyQt6.QtWidgets import QApplication, QMainWindow
from data.cidades import load_cidades
from ui.app_window import iniciar_interface

if __name__ == "__main__":
    load_cidades()
    iniciar_interface()
