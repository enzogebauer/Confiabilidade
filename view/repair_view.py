import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class RepairView(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.remove_buttons = []
        self.setWindowTitle('Cadastro de Reparos ')
        
        self.setLayout(qtw.QVBoxLayout())
        
        self.tagLabel = qtw.QLabel()
        self.layout().addWidget(self.tagLabel)
        
        self.layout().addWidget(qtw.QLabel("Tempo entre falhas"))
        self.timeBetweenFailsInputBox = qtw.QLineEdit()
        self.layout().addWidget(self.timeBetweenFailsInputBox)
        
        self.layout().addWidget(qtw.QLabel("Tempo de reparo"))
        self.repairTimeInputBox = qtw.QLineEdit()
        self.layout().addWidget(self.repairTimeInputBox)
        
        self.button = qtw.QPushButton('Cadastrar Reparo')
        self.button.clicked.connect(self.register_repair)
        self.layout().addWidget(self.button)
        
        self.repairTable = qtw.QTableWidget(0, 4)
        self.repairTable.setHorizontalHeaderLabels(['ID', 'Tempo entre falhas (dias)', 'Tempo de reparo (dias)', 'Remover'])
        self.layout().addWidget(self.repairTable)

        self.saveRepairsButton = qtw.QPushButton('Salvar Reparos')
        self.layout().addWidget(self.saveRepairsButton)

    def update_tag(self, tag):
        self.tagLabel.setText(f'Tag: {tag}')

    def register_repair(self):
        id = self.repairTable.rowCount() + 1
        time_between_fails = self.timeBetweenFailsInputBox.text()
        repair_time = self.repairTimeInputBox.text()
        self.add_repair(id, time_between_fails, repair_time)
        
        self.timeBetweenFailsInputBox.clear()
        self.repairTimeInputBox.clear()

    def add_repair(self, id, time_between_fails, repair_time):
        row = self.repairTable.rowCount()
        self.repairTable.insertRow(row)
        self.repairTable.setItem(row, 0, qtw.QTableWidgetItem(str(id)))
        self.repairTable.setItem(row, 1, qtw.QTableWidgetItem(str(time_between_fails)))
        self.repairTable.setItem(row, 2, qtw.QTableWidgetItem(str(repair_time)))
        
        remove_button = qtw.QPushButton('Remover')
        remove_button.clicked.connect(lambda: self.remove_repair(row))
        self.repairTable.setCellWidget(row, 3, remove_button)
        
        self.remove_buttons.append(remove_button)

    def remove_repair(self, row):
        if row < self.repairTable.rowCount():
            self.repairTable.removeRow(row)
            del self.remove_buttons[row]
            for i in range(row, self.repairTable.rowCount()):
                item = self.repairTable.item(i, 0)
                item.setText(str(i + 1))

    def show(self):
        super().showMaximized()