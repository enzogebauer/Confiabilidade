import controller
import PyQt5.QtWidgets as qtw
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
app = qtw.QApplication([])
controller = controller.Controller()
app.exec_()