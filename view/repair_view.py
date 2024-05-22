import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import QSize

from view_settings import ViewSettings

class RepairView(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.remove_buttons = []
        self.setWindowTitle('Cadastro de Reparos')
        self.setStyleSheet("background-color: #EDF1F7;")
        self.setLayout(qtw.QVBoxLayout())
        
        self.tagLabel = qtw.QLabel("")
        self.tagLabel.setStyleSheet("font-size: 22px; color: #000;")
        self.layout().addWidget(self.tagLabel)
        
        label1 = qtw.QLabel("Tempo entre falhas")
        label1.setStyleSheet("font-size: 22px; color: #000;")
        self.layout().addWidget(label1)
        self.timeBetweenFailsInputBox = qtw.QLineEdit()
        self.timeBetweenFailsInputBox.setValidator(qtg.QIntValidator())
        self.timeBetweenFailsInputBox.setStyleSheet("font-size: 18px; padding: 10px; color:#000")
        self.layout().addWidget(self.timeBetweenFailsInputBox)
        
        label2 = qtw.QLabel("Tempo de reparo")
        label2.setStyleSheet("font-size: 24px; color: #000;")
        self.layout().addWidget(label2)
        self.repairTimeInputBox = qtw.QLineEdit()
        self.repairTimeInputBox.setValidator(qtg.QIntValidator())
        self.repairTimeInputBox.setStyleSheet("font-size: 18px; padding: 10px; color:#000")
        self.layout().addWidget(self.repairTimeInputBox)
        
        self.button = qtw.QPushButton('Cadastrar Reparo')
        self.button.clicked.connect(self.register_repair)
        self.button.setStyleSheet("font-size: 18px; padding: 10px; background-color: #5DCFE3; color: #fff;")
        self.layout().addWidget(self.button)
        
        self.repairTable = qtw.QTableWidget(0, 4)
        self.repairTable.setHorizontalHeaderLabels(['ID', 'Tempo entre falhas (dias)', 'Tempo de reparo (dias)', 'Remover'])
        self.layout().addSpacing(20)
        # Update the header's stylesheet to change the font color to white
        self.repairTable.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #5DCFE3; color: #fff; font-size: 18px; padding: 10px;}")

        # Add these lines to resize the columns to fit the content
        header = self.repairTable.horizontalHeader()       
        header.setSectionResizeMode(0, qtw.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(2, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(3, qtw.QHeaderView.ResizeToContents)

        self.repairTable.setStyleSheet("selection-background-color: #5DCFE3; color: #000;")
        self.layout().addWidget(self.repairTable)

        self.saveRepairsButton = qtw.QPushButton('Salvar Rrrreparos')
        self.saveRepairsButton.setStyleSheet("font-size: 18px; padding: 10px; background-color: #5DCFE3; color: #fff;")
        self.layout().addWidget(self.saveRepairsButton)

        # Aplicando as configurações padrão
        ViewSettings.apply_settings(self)

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
                button = self.remove_buttons[i]
                button.disconnect()
                button.clicked.connect(lambda _checked, i=i: self.remove_repair(i))