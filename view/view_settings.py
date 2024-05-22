from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QDesktopWidget

class ViewSettings:
    @staticmethod
    def apply_settings(window):
        # Definindo o tamanho da janela
        window.setFixedSize(QSize(800, 600))