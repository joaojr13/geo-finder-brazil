from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QWidget, QCompleter, QComboBox, QMessageBox, QHBoxLayout, QTreeWidget, QTreeWidgetItem
)
from PyQt6.QtCore import Qt
from data.cidades import get_lista_cidades_unicas
from controllers.search_controller import buscar_coordenadas


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Busca de Coordenadas")
        self.setFixedSize(700, 300)

        self.resultado_label = QLabel("")
        self.resultado_label.setWordWrap(True)

        self.cidade_input = QLineEdit()
        self.cidade_input.setPlaceholderText("Digite o nome da cidade")

        self.estado_input = QComboBox()

        self.buscar_btn = QPushButton("Buscar Coordenadas")
        self.buscar_btn.clicked.connect(self.ao_clicar)

        # Histórico de pesquisas
        self.historico_tree = QTreeWidget()
        self.historico_tree.setHeaderLabel("Histórico de Pesquisas")
        self.historico_tree.itemClicked.connect(self.ao_clicar_historico)

        # Configurar autocomplete
        cidades = get_lista_cidades_unicas()
        completer = QCompleter(cidades)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.cidade_input.setCompleter(completer)

        # Layout
        formulario = QVBoxLayout()
        formulario.addWidget(QLabel("Cidade:"))
        formulario.addWidget(self.cidade_input)
        formulario.addWidget(QLabel("Estado:"))
        formulario.addWidget(self.estado_input)
        formulario.addWidget(self.buscar_btn)
        formulario.addWidget(self.resultado_label)

        layout_principal = QHBoxLayout()
        layout_principal.addLayout(formulario)
        layout_principal.addWidget(self.historico_tree)

        container = QWidget()
        container.setLayout(layout_principal)
        self.setCentralWidget(container)

    def mostrar_popup(self, titulo, mensagem):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensagem)
        msg_box.exec()

    def adicionar_item_historico(self, cidade, estado, lat, lon):
        texto = f"{cidade} - {estado}"
        node = QTreeWidgetItem([texto])
        node.setData(0, Qt.ItemDataRole.UserRole, (lat, lon))

        lat_item = QTreeWidgetItem([f"Latitude: {lat}"])
        lon_item = QTreeWidgetItem([f"Longitude: {lon}"])
        node.addChild(lat_item)
        node.addChild(lon_item)

        self.historico_tree.insertTopLevelItem(0, node)

    def ao_clicar_historico(self, item):
        if item.parent() is not None:
            return
        lat, lon = item.data(0, Qt.ItemDataRole.UserRole)
        cidade_estado = item.text(0)
        self.resultado_label.setText(f"{cidade_estado}\nLatitude: {lat}\nLongitude: {lon}")

    def ao_clicar(self):
        nome = self.cidade_input.text()
        estado = self.estado_input.currentText()
        if not nome:
            self.mostrar_popup("Aviso", "Digite o nome da cidade.")
            return

        resultado = buscar_coordenadas(nome, estado)

        print(resultado)
        if len(resultado) > 1:
            self.estado_input.clear()

            for dict in resultado:
                self.estado_input.addItem(dict["estado"].strip())

            self.estado_input.setEnabled(True)
            # self.resultado_label.setText("Cidade encontrada em múltiplos estados. Selecione um.")
            self.mostrar_popup("Atenção", "Cidade encontrada em múltiplos estados. Selecione um.")
        else:
            cidade = resultado[0]["cidade"]
            estado = resultado[0]["estado"]
            lat, lon = resultado[0]["coordenadas"]
            msg = f"{cidade} - {estado}\nLatitude: {lat}\nLongitude: {lon}"
            self.mostrar_popup("Resultado encontrado", msg)
            self.estado_input.setEnabled(False)
            self.resultado_label.clear()
            self.estado_input.clear()
            self.adicionar_item_historico(cidade, estado, lat, lon)


def iniciar_interface():
    import sys
    app = QApplication(sys.argv)
    janela = AppWindow()
    janela.show()
    sys.exit(app.exec())