import sys
sys.path.extend(['./model', './view', './controller'])
from controller import Controller
import PyQt5.QtWidgets as qtw

if __name__ == '__main__':
    app = qtw.QApplication([])
    controller = Controller()
    app.exec_()