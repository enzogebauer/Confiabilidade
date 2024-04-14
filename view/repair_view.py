import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class RepairView(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # Add a list to store the remove buttons
        self.remove_buttons = []
        self.setWindowTitle('Cadastro de Reparos ')
        
        self.setLayout(qtw.QVBoxLayout())
        
        # Add a QLabel to display the tag
        self.tagLabel = qtw.QLabel()
        self.layout().addWidget(self.tagLabel)
        
        self.layout().addWidget(qtw.QLabel("Tempo entre falhas"))
        self.timeBetweenFailsInputBox = qtw.QLineEdit()
        self.layout().addWidget(self.timeBetweenFailsInputBox)
        
        self.layout().addWidget(qtw.QLabel("Tempo de reparo"))
        self.repairTimeInputBox = qtw.QLineEdit()
        self.layout().addWidget(self.repairTimeInputBox)
        
        self.button = qtw.QPushButton('Cadastrar Reparo')
        self.button.clicked.connect(self.register_repair)  # Connect the button's clicked signal to the register_repair method
        self.layout().addWidget(self.button)
        
        # Add a QTableWidget to display the repairs
        self.repairTable = qtw.QTableWidget(0, 4)  # 0 rows, 4 columns
        self.repairTable.setHorizontalHeaderLabels(['ID', 'Tempo entre falhas (dias)', 'Tempo de reparo (dias)', 'Remover'])
        self.layout().addWidget(self.repairTable)

    def update_tag(self, tag):
        self.tagLabel.setText(f'Tag: {tag}')  # Update the text of the tagLabel with the tag

    def register_repair(self):
        id = self.repairTable.rowCount() + 1  # Generate the ID
        time_between_fails = self.timeBetweenFailsInputBox.text()
        repair_time = self.repairTimeInputBox.text()
        self.add_repair(id, time_between_fails, repair_time)
        
        # Clear the input boxes
        self.timeBetweenFailsInputBox.clear()
        self.repairTimeInputBox.clear()

    def add_repair(self, id, time_between_fails, repair_time):
        row = self.repairTable.rowCount()
        self.repairTable.insertRow(row)
        self.repairTable.setItem(row, 0, qtw.QTableWidgetItem(str(id)))
        self.repairTable.setItem(row, 1, qtw.QTableWidgetItem(str(time_between_fails)))
        self.repairTable.setItem(row, 2, qtw.QTableWidgetItem(str(repair_time)))
        
        # Add a remove button
        remove_button = qtw.QPushButton('Remover')
        remove_button.clicked.connect(lambda: self.remove_repair(row))
        self.repairTable.setCellWidget(row, 3, remove_button)
        
        # Add the remove button to the list
        self.remove_buttons.append(remove_button)

    def remove_repair(self, row):
      if row < self.repairTable.rowCount():
          self.repairTable.removeRow(row)
          
          # Remove the button from the list
          del self.remove_buttons[row]
          
          # Update the IDs of all rows below the removed row
          for i in range(row, self.repairTable.rowCount()):
              item = self.repairTable.item(i, 0)  # Get the ID item
              item.setText(str(i + 1))  # Update the ID

    def show(self):
        super().showMaximized()  # Show the window maximized