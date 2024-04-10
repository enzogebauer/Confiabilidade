import sqlite3
import uuid
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cadastro de Componentes')
        
        # Set the vertical layout
        self.setLayout(qtw.QVBoxLayout())
        
        # Create a label and input box for Tag
        self.layout().addWidget(qtw.QLabel("Tag"))
        self.tagInputBox = qtw.QLineEdit()
        self.tagInputBox.setObjectName('tag')
        self.layout().addWidget(self.tagInputBox)
        
        # Create a label and input box for Description
        self.layout().addWidget(qtw.QLabel("Descrição"))
        self.descInputBox = qtw.QLineEdit()
        self.descInputBox.setObjectName('description')
        self.layout().addWidget(self.descInputBox)
        
        # Create a register button
        button = qtw.QPushButton('Cadastrar', clicked = self.register_component)
        self.layout().addWidget(button)
        
        # Initialize the database
        self.conn = sqlite3.connect('components.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS Component
                          (id text PRIMARY KEY, tag text, description text)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS Repair
                          (repair_id text PRIMARY KEY, time_between_fails text, repair_time text, component_id text,
                          FOREIGN KEY(component_id) REFERENCES Component(id))''')
        
        self.show()

    def register_component(self):
        # Get the tag and description from the input boxes
        tag = self.tagInputBox.text()
        description = self.descInputBox.text()
        
        # Generate a UUID for the component
        id = str(uuid.uuid4())
        
        # Insert the component into the database
        self.c.execute("INSERT INTO Component VALUES (?, ?, ?)", (id, tag, description))
        self.conn.commit()
        
        # Print the component
        print(f'Componente cadastrado -> ID: {id}, Tag: {tag}, Descrição: {description}')

    # Other CRUD operations for Component and Repair tables...

app = qtw.QApplication([])
mw = MainWindow()
app.exec_()