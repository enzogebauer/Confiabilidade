from model import Model
from view.view import View
from view.repair_view import RepairView

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.repairView = RepairView()
        self.view.button.clicked.connect(self.register_component)
        self.view.show() 

    def register_component(self):
        tag = self.view.tagInputBox.text()
        description = self.view.descInputBox.text()
        id, tag, description = self.model.register_component(tag, description)
        print(f'Componente cadastrado -> ID: {id}, Tag: {tag}, Descrição: {description}')
        self.view.hide()
        self.repairView.update_tag(tag)
        self.repairView.show()