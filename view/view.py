import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import QSize

from view_settings import ViewSettings

class View(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cadastro de Componentes')
        self.setStyleSheet("background-color: #EDF1F7;")
        self.setLayout(qtw.QVBoxLayout())
        
        # Create a header with a large title
        header = qtw.QLabel("Cadastro de Componentes")
        header.setStyleSheet("font-size: 32px; color: #000; qproperty-alignment: AlignCenter; padding: 20px; background-color: #5DCFE3;")
        self.layout().addWidget(header)
        
        grid = qtw.QGridLayout()
        self.layout().addLayout(grid)
        
        tagLabel = qtw.QLabel("Tag")
        tagLabel.setStyleSheet("font-size: 22px; color: #000;")
        grid.addWidget(tagLabel, 0, 0, 1, 2)  # Place the label above the input box
        self.tagInputBox = qtw.QLineEdit()
        self.tagInputBox.setStyleSheet("font-size: 18px; padding: 10px; color:#000")
        grid.addWidget(self.tagInputBox, 1, 0, 1, 2)  # Place the input box below the label
        
        grid.setRowStretch(2, 1)  # Add an empty space after the input box
        
        descLabel = qtw.QLabel("Descrição")
        descLabel.setStyleSheet("font-size: 22px; color: #000;")
        grid.addWidget(descLabel, 3, 0, 1, 2)  # Place the label above the input box
        self.descInputBox = qtw.QLineEdit()
        self.descInputBox.setStyleSheet("font-size: 18px; padding: 10px; color:#000")
        grid.addWidget(self.descInputBox, 4, 0, 1, 2)  # Place the input box below the label
        
        grid.setRowStretch(5, 1)  # Add an empty space after the input box
        
        self.button = qtw.QPushButton('Cadastrar')
        self.button.setStyleSheet("font-size: 18px; padding: 10px; background-color: #5DCFE3; color: #fff;")
        grid.addWidget(self.button, 6, 0, 1, 2)

        # Aplicando as configurações padrão
        ViewSettings.apply_settings(self)