import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class MainWindow(qtw.QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Hello World')
    
    # Set the vertical layout
    self.setLayout(qtw.QVBoxLayout())
    
    #Create a basic label
    label = qtw.QLabel("HELLO THERE, WHAT'S YOUR NAME ?")
    #chage the font size of label
    label.setFont(qtg.QFont('Arial', 24))
    self.layout().addWidget(label)
    #Create an input box
    inputBox = qtw.QLineEdit()
    inputBox.setObjectName('name')
    inputBox.setFont(qtg.QFont('Arial', 24))
    self.layout().addWidget(inputBox)
    #display name inputted 
    button = qtw.QPushButton('Submit', clicked = lambda: print(f'Nome salvo ->  {inputBox.text()}'))
    self.layout().addWidget(button)
    
    self.show()

app = qtw.QApplication([])
mw = MainWindow()
app.exec_()