import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class View(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cadastro de Componentes')
        
        self.setLayout(qtw.QVBoxLayout())
        
        self.layout().addWidget(qtw.QLabel("Tag"))
        self.tagInputBox = qtw.QLineEdit()
        self.layout().addWidget(self.tagInputBox)
        
        self.layout().addWidget(qtw.QLabel("Descrição"))
        self.descInputBox = qtw.QLineEdit()
        self.layout().addWidget(self.descInputBox)
        
        self.button = qtw.QPushButton('Cadastrar')
        self.layout().addWidget(self.button)
        
        self.show()