import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QValidator
from PyQt5.QtCore import Qt, pyqtSignal

class PercentValidator(QValidator):
    def validate(self, input, pos):
        # Remove the '%' sign to validate the number
        if input.endswith('%'):
            input = input[:-1]

        if input == '':
            return QValidator.Intermediate, input, pos

        try:
            value = float(input)
            if 0 <= value <= 100:
                return QValidator.Acceptable, input + '%', pos
            else:
                return QValidator.Invalid, input, pos
        except ValueError:
            return QValidator.Invalid, input, pos

    def fixup(self, input):
        # Add the '%' sign if it's missing
        if not input.endswith('%'):
            return input + '%'
        return input

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

        # Adicionar botão realizeAnalysis no final
        self.realizeAnalysis = QPushButton('Realizar Análise')
        self.realizeAnalysis.setStyleSheet("font-size: 18px; padding: 10px; background-color: #5DCFE3; color: #fff;")
        self.layout.addWidget(self.realizeAnalysis, alignment=Qt.AlignBottom)

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
            self.layout.insertWidget(self.layout.count() - 1, title_label, alignment=Qt.AlignCenter)

            if distribution_parameters:
                # Adicionar parâmetros da distribuição
                params_label = QLabel(self)
                params_label.setText(f"Parâmetros: {distribution_parameters}")
                self.layout.insertWidget(self.layout.count() - 1, params_label, alignment=Qt.AlignCenter)

            # Adicionar a imagem
            label = QLabel(self)
            pixmap = QPixmap(image_path)
            label.setPixmap(pixmap)
            # self.layout.insertWidget(self.layout.count() - 1, label, alignment=Qt.AlignCenter)

            # Adicionar Labels e InputBox
            v_layout = QVBoxLayout()

            inputLabel = QLabel("Confiabilidade")
            inputLabel.setStyleSheet("font-size: 16px; color: #000;")
            v_layout.addWidget(inputLabel)

            self.inputBox = QLineEdit()
            self.inputBox.setValidator(PercentValidator())
            self.inputBox.setPlaceholderText("Qual a probabilidade mínima que você deseja para a confiabilidade")
            self.inputBox.setStyleSheet("font-size: 18px; padding: 10px; color:#000")
            v_layout.addWidget(self.inputBox)

            responseLabel = QLabel("Tempo até o percentual da falha")
            responseLabel.setStyleSheet("font-size: 22px; color: #000;")
            v_layout.addWidget(responseLabel)

            self.responseOutput = QLabel("")
            self.responseOutput.setStyleSheet("font-size: 22px; color: #000;")
            v_layout.addWidget(self.responseOutput)

            '''self.analysisButton = QPushButton('Analisar')
            self.analysisButton.setStyleSheet("font-size: 18px; padding: 10px; background-color: #5DCFE3; color: #fff;")
            v_layout.addWidget(self.analysisButton)'''
            
            h_layout = QHBoxLayout()
            h_layout.addWidget(label)
            h_layout.addLayout(v_layout)

            self.layout.insertLayout(self.layout.count() - 1, h_layout)

        else:
            print(f"Imagem {image_path} não encontrada.")

    def show(self):
        super().showMaximized()
