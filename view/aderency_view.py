import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal
import matplotlib.pyplot as plt


class AderencyView(QWidget):
    shown = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teste de Aderência")
        self.setStyleSheet("background-color: #EDF1F7;")

        # Configurar área de rolagem
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Widget central com layout vertical
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.central_widget)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.shown.emit()

    def display_image(self, image_path, title, distribution_parameters=None):
        if os.path.exists(image_path):
            # Adicionar título da imagem
            title_label = QLabel(self)
            title_label.setText(title)
            title_label.setFont(QFont("Arial", 24))
            # Set text color to black
            title_label.setStyleSheet("color: black;")  # Apply inline style
            self.layout.addWidget(title_label, alignment=Qt.AlignCenter)

            if distribution_parameters:
                # Adicionar parâmetros da distribuição
                params_label = QLabel(self)
                params_label.setText(f"Parâmetros: {distribution_parameters}")
                self.layout.addWidget(params_label, alignment=Qt.AlignCenter)

            # Adicionar a imagem
            label = QLabel(self)
            pixmap = QPixmap(image_path)
            label.setPixmap(pixmap)
            self.layout.addWidget(label, alignment=Qt.AlignCenter)
        else:
            print(f"Imagem {image_path} não encontrada.")

    def show(self):
        super().showMaximized()
