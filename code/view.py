import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

class View(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cadastro de Componentes')
        self.setStyleSheet("background-color: #EDF1F7;")
        
        # Layout principal
        main_layout = qtw.QVBoxLayout()
        self.setLayout(main_layout)

        # Header
        header_container = qtw.QWidget()
        header_container.setStyleSheet("background-color: #5DCFE3;")
        header_container.setMinimumHeight(200)
        header_layout = qtw.QHBoxLayout()
        header_container.setLayout(header_layout)

        header = qtw.QLabel("Cadastro de Componentes")
        header.setStyleSheet("font-size: 48px; font-family: 'Berlin Sans FB Demi'; color: #FFF; padding: 20px; qproperty-alignment: AlignCenter;")
        header_layout.addWidget(header)

        main_layout.addWidget(header_container)

        # Main content area
        content_container = qtw.QWidget()
        content_layout = qtw.QVBoxLayout()
        content_layout.setAlignment(qtc.Qt.AlignCenter)
        content_container.setLayout(content_layout)
        main_layout.addWidget(content_container)

        grid = qtw.QGridLayout()
        content_layout.addLayout(grid)

        grid.setRowStretch(0, 1)

        tagLabel = qtw.QLabel("Tag")
        tagLabel.setStyleSheet("font-size: 22px; font-family: 'Berlin Sans FB'; color: #000;")
        grid.addWidget(tagLabel, 1, 0, 1, 2)  # Place the label above the input box

        self.tagInputBox = qtw.QLineEdit()
        self.tagInputBox.setStyleSheet("font-size: 18px; padding: 10px; background-color:#FFF; color:#000; border: none; outline: none;")
        self.tagInputBox.setMinimumHeight(75)
        self.tagInputBox.setMinimumWidth(400)
        grid.addWidget(self.tagInputBox, 2, 0, 1, 2)  # Place the input box below the label

        descLabel = qtw.QLabel("Descrição")
        descLabel.setStyleSheet("font-size: 22px; font-family: 'Berlin Sans FB'; color: #000;")
        grid.addWidget(descLabel, 3, 0, 1, 2)  # Place the label above the input box

        self.descInputBox = qtw.QLineEdit()
        self.descInputBox.setStyleSheet("font-size: 18px; padding: 10px; background-color:#FFF; color:#000; border: none; outline: none;")
        self.descInputBox.setMinimumHeight(75)
        self.descInputBox.setMinimumWidth(400)
        grid.addWidget(self.descInputBox, 4, 0, 1, 2)  # Place the input box below the label

        self.button = qtw.QPushButton('Cadastrar')
        self.button.setStyleSheet("font-size: 28px; font-family: 'Berlin Sans FB Demi'; padding: 10px; background-color: #5DCFE3; color: #fff; border: none; outline: none;")
        self.button.setMinimumHeight(75)
        self.button.setMaximumWidth(200)
        
        # Create a container for the button with a QHBoxLayout to center it
        button_container = qtw.QWidget()
        button_layout = qtw.QHBoxLayout(button_container)
        button_layout.setAlignment(qtc.Qt.AlignCenter)
        button_layout.addWidget(self.button)
        grid.addWidget(button_container, 5, 0, 1, 2)

        grid.setRowStretch(6, 1)

    def show(self):
        super().showMaximized()  # Show the window maximized