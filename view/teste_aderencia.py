import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QScrollArea
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from controller.testeDeAderenciaFinal import compare_distributions

class TesteAderencia(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Teste de Aderência')
        self.setStyleSheet("background-color: #EDF1F7;")

        # Criar uma área de rolagem
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Criar o widget central para o layout
        central_widget = QWidget()
        self.layout = QVBoxLayout(central_widget)
        self.layout.setAlignment(Qt.AlignTop)  # Alinhar widgets ao topo
        
        # Adicionar o widget central à área de rolagem
        scroll_area.setWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        self.run_test_and_show_results()

    def run_test_and_show_results(self):
        # Run the test to generate the plots
        fail_times = [24, 38, 56, 85, 122, 157, 240, 470, 680, 930, 1320, 1655]
        compare_distributions(fail_times)

        # Display the plots
        self.display_image('weibull_reliability.png', 'Weibull Distribution Reliability')
        self.display_image('lognormal_reliability.png', 'Lognormal Distribution Reliability')

    def display_image(self, image_path, title):
        if os.path.exists(image_path):
            title_label = QLabel(self)
            title_label.setText(title)
            title_label.setFont(QFont('Arial', 14))
            self.layout.addWidget(title_label, alignment=Qt.AlignCenter)
            
            label = QLabel(self)
            pixmap = QPixmap(image_path)
            label.setPixmap(pixmap)
            self.layout.addWidget(label, alignment=Qt.AlignCenter)
        else:
            print(f"Imagem {image_path} não encontrada.")