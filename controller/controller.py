from model import Model
from view import View

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.view.button.clicked.connect(self.register_component)

    def register_component(self):
        tag = self.view.tagInputBox.text()
        description = self.view.descInputBox.text()
        id, tag, description = self.model.register_component(tag, description)
        print(f'Componente cadastrado -> ID: {id}, Tag: {tag}, Descrição: {description}')