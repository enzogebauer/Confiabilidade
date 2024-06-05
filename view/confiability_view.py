import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import QSize

from PyQt5 import QtCore, QtGui, QtWidgets

# from view_settings import ViewSettings

class ConfiabilityView(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Análise de Confiabilidade')
        self.setStyleSheet("background-color: #EDF1F7;")
        self.setLayout(qtw.QVBoxLayout())

        # Header
        header = qtw.QLabel("Realizar Análise")
        header.setStyleSheet("font-size: 32px; font-family: Berlin Sans; color: #FFF; qproperty-alignment: AlignCenter; padding: 20px; background-color: #5DCFE3;")
        self.layout().addWidget(header)

        grid = qtw.QGridLayout()
        self.layout().addLayout(grid)

        inputLabel = qtw.QLabel("Confiabilidade")
        inputLabel.setStyleSheet("font-size: 16px; color: #000;")
        grid.addWidget(inputLabel, 0, 0, 1, 2)  # Place the label above the input box
        self.inputBox = qtw.QLineEdit()
        self.inputBox.setValidator(qtg.QDoubleValidator(0.0, 100.0, 2))
        self.inputBox.setPlaceholderText("Qual a probabilidade mínima que você deseja para a confiabilidade")
        self.inputBox.setStyleSheet("font-size: 18px; padding: 10px; color:#000")
        grid.addWidget(self.inputBox, 1, 0, 1, 2)  # Place the input box below the label

        grid.setRowStretch(2, 1)  # Add an empty space after the input box

        responseLabel = qtw.QLabel("Tempo até o percentual da falha")
        responseLabel.setStyleSheet("font-size: 22px; color: #000;")
        grid.addWidget(responseLabel, 3, 0, 1, 2)  # Place the label above the input box
        self.responseOutput = qtw.QLabel("")
        self.responseOutput.setStyleSheet("font-size: 22px; color: #000;")
        grid.addWidget(self.responseOutput, 4, 0, 1, 2)  # Place the input box below the label

        grid.setRowStretch(5, 1)  # Add an empty space after the input box
        
        self.registerButton = qtw.QPushButton('Analisar')
        self.registerButton.setStyleSheet("font-size: 18px; padding: 10px; background-color: #5DCFE3; color: #fff;")
        grid.addWidget(self.registerButton, 6, 0, 1, 2)

        grid.setRowStretch(7, 1)
    
    def show(self):
        super().showMaximized()