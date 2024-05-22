import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import re
from fractions import Fraction

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
        self.timeBetweenFailsInputBox.setStyleSheet("font-size: 18px; padding: 10px; color:#000")
        self.layout().addWidget(self.timeBetweenFailsInputBox)
        
        self.tbfUnitSelector = qtw.QComboBox()
        self.tbfUnitSelector.addItems(["horas", "dias"])
        self.tbfUnitSelector.setStyleSheet("font-size: 18px; padding: 10px; color:#000; background-color:#5DCFE3;")
        self.layout().addWidget(self.tbfUnitSelector)
        
        label2 = qtw.QLabel("Tempo de reparo")
        label2.setStyleSheet("font-size: 24px; color: #000;")
        self.layout().addWidget(label2)
        self.repairTimeInputBox = qtw.QLineEdit()
        self.repairTimeInputBox.setStyleSheet("font-size: 18px; padding: 10px; color:#000")
        self.layout().addWidget(self.repairTimeInputBox)
        
        self.rtUnitSelector = qtw.QComboBox()
        self.rtUnitSelector.addItems(["horas", "dias"])
        self.rtUnitSelector.setStyleSheet("font-size: 18px; padding: 10px; color:#000; background-color:#5DCFE3;")
        self.layout().addWidget(self.rtUnitSelector)
        
        self.button = qtw.QPushButton('Cadastrar Reparo')
        self.button.clicked.connect(self.register_repair)
        self.button.setStyleSheet("font-size: 18px; padding: 10px; background-color: #5DCFE3; color: #fff;")
        self.layout().addWidget(self.button)
        
        self.repairTable = qtw.QTableWidget(0, 6)
        self.repairTable.setHorizontalHeaderLabels(['ID', 'Tempo entre falhas', 'Unidade de tempo entre falhas', 'Tempo de reparo', 'Unidade de tempo de reparo', 'Remover'])
        self.layout().addSpacing(20)
        # Update the header's stylesheet to change the font color to white
        self.repairTable.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #5DCFE3; color: #fff; font-size: 18px; padding: 10px;}")

        # Add these lines to resize the columns to fit the content
        header = self.repairTable.horizontalHeader()       
        header.setSectionResizeMode(0, qtw.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(2, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(3, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(4, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(5, qtw.QHeaderView.ResizeToContents)

        self.repairTable.setStyleSheet("selection-background-color: #5DCFE3; color: #000;")
        self.layout().addWidget(self.repairTable)

        self.saveRepairsButton = qtw.QPushButton('Salvar Reparos')
        self.saveRepairsButton.setStyleSheet("font-size: 18px; padding: 10px; background-color: #5DCFE3; color: #fff;")
        self.layout().addWidget(self.saveRepairsButton)

        # Set the regex validators
        regex = qtc.QRegExp(r'^\d+(\.\d+)?(/\d+(\.\d+)?)?$')
        validator = qtg.QRegExpValidator(regex)
        self.timeBetweenFailsInputBox.setValidator(validator)
        self.repairTimeInputBox.setValidator(validator)

    def update_tag(self, tag):
        self.tagLabel.setText(f'Tag: {tag}')

    def register_repair(self):
        time_between_fails = self.parse_input(self.timeBetweenFailsInputBox.text())
        tbf_unit = self.tbfUnitSelector.currentText()
        repair_time = self.parse_input(self.repairTimeInputBox.text())
        rt_unit = self.rtUnitSelector.currentText()

        if not self.validate_units(tbf_unit, rt_unit):
            qtw.QMessageBox.warning(self, "Unidade de Tempo Inválida", "Só é possível inserir dados de uma unidade de tempo por coluna.")
            return

        id = self.repairTable.rowCount() + 1
        self.add_repair(id, str(time_between_fails), tbf_unit, str(repair_time), rt_unit)

        self.timeBetweenFailsInputBox.clear()
        self.repairTimeInputBox.clear()

    def validate_units(self, tbf_unit, rt_unit):
        existing_tbf_units = set(self.get_column_units(2))
        existing_rt_units = set(self.get_column_units(4))

        if (existing_tbf_units and tbf_unit not in existing_tbf_units) or (existing_rt_units and rt_unit not in existing_rt_units):
            return False
        return True
    def get_column_units(self, column_index):
        units = []
        for row in range(self.repairTable.rowCount()):
            item = self.repairTable.item(row, column_index)
            if item:
                units.append(item.text())
        return units

    def parse_input(self, input_str):
        try:
            if ('/' in input_str) and (input_str.count('/') == 1):
                return float(Fraction(input_str))
            else:
                return float(input_str)
        except ValueError:
            return None

    def add_repair(self, id, time_between_fails, tbf_unit, repair_time, rt_unit):
        row = self.repairTable.rowCount()
        self.repairTable.insertRow(row)
        self.add_non_editable_item(row, 0, str(id))
        self.add_non_editable_item(row, 1, str(time_between_fails))
        self.add_non_editable_item(row, 2, tbf_unit)
        self.add_non_editable_item(row, 3, str(repair_time))
        self.add_non_editable_item(row, 4, rt_unit)
        
        remove_button = qtw.QPushButton('Remover')
        remove_button.clicked.connect(lambda: self.remove_repair(row))
        self.repairTable.setCellWidget(row, 5, remove_button)
        self.remove_buttons.append(remove_button)

    def add_non_editable_item(self, row, column, text):
        item = qtw.QTableWidgetItem(text)
        item.setFlags(item.flags() & ~qtc.Qt.ItemIsEditable)
        self.repairTable.setItem(row, column, item)

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

    def show(self):
        super().showMaximized()
