import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as QtCore

class PercentValidator(qtg.QValidator):
    def validate(self, input, pos):
        # Remove the '%' sign to validate the number
        if input.endswith('%'):
            input = input[:-1]

        if input == '':
            return qtg.QValidator.Intermediate, input, pos

        try:
            value = float(input)
            if 0 <= value <= 100:
                return qtg.QValidator.Acceptable, input + '%', pos
            else:
                return qtg.QValidator.Invalid, input, pos
        except ValueError:
            return qtg.QValidator.Invalid, input, pos

    def fixup(self, input):
        # Add the '%' sign if it's missing
        if not input.endswith('%'):
            return input + '%'
        return input

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
        self.inputBox.setValidator(PercentValidator())
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

if __name__ == '__main__':
    app = qtw.QApplication([])
    mainWin = ConfiabilityView()
    mainWin.show()
    app.exec_()
