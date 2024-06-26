import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from fractions import Fraction


class RepairView(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.remove_buttons = []
        self.setWindowTitle("Cadastro de Reparos")
        self.setStyleSheet("background-color: #EDF1F7;")
        self.setLayout(qtw.QVBoxLayout())

        self.tagLabel = qtw.QLabel("")
        self.tagLabel.setStyleSheet("font-size: 22px; color: #000;")
        self.layout().addWidget(self.tagLabel)

        label1 = qtw.QLabel("Tempo entre falhas")
        label1.setStyleSheet("font-size: 22px; color: #000;")
        self.layout().addWidget(label1)
        self.timeBetweenFailsInputBox = qtw.QLineEdit()
        self.timeBetweenFailsInputBox.setStyleSheet(
            "font-size: 18px; padding: 10px; color:#000"
        )
        self.layout().addWidget(self.timeBetweenFailsInputBox)

        self.tbfUnitSelector = qtw.QComboBox()
        self.tbfUnitSelector.addItems(["horas", "dias"])
        self.tbfUnitSelector.setStyleSheet(
            "font-size: 18px; padding: 10px; color:#000; background-color:#5DCFE3;"
        )
        self.layout().addWidget(self.tbfUnitSelector)

        label2 = qtw.QLabel("Tempo de reparo")
        label2.setStyleSheet("font-size: 24px; color: #000;")
        self.layout().addWidget(label2)
        self.repairTimeInputBox = qtw.QLineEdit()
        self.repairTimeInputBox.setStyleSheet(
            "font-size: 18px; padding: 10px; color:#000"
        )
        self.layout().addWidget(self.repairTimeInputBox)

        self.rtUnitSelector = qtw.QComboBox()
        self.rtUnitSelector.addItems(["horas", "dias"])
        self.rtUnitSelector.setStyleSheet(
            "font-size: 18px; padding: 10px; color:#000; background-color:#5DCFE3;"
        )
        self.layout().addWidget(self.rtUnitSelector)

        self.button = qtw.QPushButton("Cadastrar Reparo")
        self.button.clicked.connect(self.register_repair)
        self.button.setStyleSheet(
            "font-size: 18px; padding: 10px; background-color: #5DCFE3; color: #fff;"
        )
        self.layout().addWidget(self.button)

        self.repairTable = qtw.QTableWidget(0, 6)
        self.repairTable.setHorizontalHeaderLabels(
            [
                "ID",
                "Tempo entre falhas",
                "Unidade TEF",
                "Tempo de reparo",
                "Unidade TR",
                "Remover",
            ]
        )
        self.layout().addSpacing(20)
        self.repairTable.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #5DCFE3; color: #fff; font-size: 18px; padding: 10px;}"
        )

        header = self.repairTable.horizontalHeader()
        header.setSectionResizeMode(0, qtw.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(2, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(3, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(4, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(5, qtw.QHeaderView.ResizeToContents)

        self.repairTable.setStyleSheet(
            "selection-background-color: #5DCFE3; color: #000;"
        )
        self.layout().addWidget(self.repairTable)

        self.saveRepairsButton = qtw.QPushButton("Salvar Reparos")
        self.saveRepairsButton.setStyleSheet(
            "font-size: 18px; padding: 10px; background-color: #5DCFE3; color: #fff;"
        )
        self.layout().addWidget(self.saveRepairsButton)

        regex = qtc.QRegExp(r"^\d+(\.\d+)?(/\d+(\.\d+)?)?$")
        validator = qtg.QRegExpValidator(regex)
        self.timeBetweenFailsInputBox.setValidator(validator)
        self.repairTimeInputBox.setValidator(validator)

    def update_tag(self, tag):
        self.tagLabel.setText(f"Tag: {tag}")

    def register_repair(self):
        time_between_fails = self.parse_input(self.timeBetweenFailsInputBox.text())
        tbf_unit = self.tbfUnitSelector.currentText()
        repair_time = self.parse_input(self.repairTimeInputBox.text())
        rt_unit = self.rtUnitSelector.currentText()
        if time_between_fails is None or repair_time is None:
            qtw.QMessageBox.warning(
                self,
                "Valor Inválido",
                "Por favor, insira um valor válido para o tempo entre falhas e o tempo de reparo.",
            )
            return
        if not self.validate_units(tbf_unit, rt_unit):
            qtw.QMessageBox.warning(
                self,
                "Unidade de Tempo Inválida",
                "Só é possível inserir dados de uma unidade de tempo por coluna.",
            )
            return

        id = self.repairTable.rowCount() + 1
        self.add_repair(id, time_between_fails, tbf_unit, repair_time, rt_unit)

        self.timeBetweenFailsInputBox.clear()
        self.repairTimeInputBox.clear()

    def validate_units(self, tbf_unit, rt_unit):
# If the table is empty, any unit is valid
        if self.repairTable.rowCount() == 0:
            return True

        # Get the units already in the table for TBF and RT columns
        tbf_units_in_table = self.get_column_units(2)
        rt_units_in_table = self.get_column_units(4)

        # If there are units in the table, check if the new units match the existing ones
        if tbf_units_in_table and rt_units_in_table:
            return all(unit == tbf_units_in_table[0] for unit in tbf_units_in_table) and \
                all(unit == rt_units_in_table[0] for unit in rt_units_in_table) and \
                tbf_unit == tbf_units_in_table[0] and rt_unit == rt_units_in_table[0]

        # If the table has units but they are inconsistent, or the new units don't match, return False
        return False
    def get_column_units(self, column_index):
        units = []
        for row in range(self.repairTable.rowCount()):
            item = self.repairTable.item(row, column_index)
            if item:
                units.append(item.text())
        return units

    def parse_input(self, input_str):
        try:
            if "/" in input_str:
                return float(Fraction(input_str))
            else:
                return float(input_str)
        except ValueError:
            return None

    def add_repair(self, id, time_between_fails, tbf_unit, repair_time, rt_unit):
        row = self.repairTable.rowCount()
        self.repairTable.insertRow(row)
        self.repairTable.setItem(row, 0, qtw.QTableWidgetItem(str(id)))
        self.repairTable.setItem(row, 1, qtw.QTableWidgetItem(str(time_between_fails)))

        tbf_unit_item = qtw.QTableWidgetItem(str(tbf_unit))
        tbf_unit_item.setFlags(tbf_unit_item.flags() ^ qtc.Qt.ItemIsEditable)
        self.repairTable.setItem(row, 2, tbf_unit_item)

        self.repairTable.setItem(row, 3, qtw.QTableWidgetItem(str(repair_time)))

        rt_unit_item = qtw.QTableWidgetItem(rt_unit)
        rt_unit_item.setFlags(rt_unit_item.flags() ^ qtc.Qt.ItemIsEditable)
        self.repairTable.setItem(row, 4, rt_unit_item)

        remove_button = qtw.QPushButton("Remover")
        remove_button.clicked.connect(lambda: self.remove_repair(row))
        self.repairTable.setCellWidget(row, 5, remove_button)
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

    def show(self):
        super().showMaximized()