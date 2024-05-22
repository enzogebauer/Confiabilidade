from model import Model
from view.view import View
from view.repair_view import RepairView
import uuid

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.repairView = RepairView()
        self.view.button.clicked.connect(self.register_component)
        self.repairView.saveRepairsButton.clicked.connect(self.register_repairs)
        self.view.show()

    def register_component(self):
        tag = self.view.tagInputBox.text()
        description = self.view.descInputBox.text()
        self.component_id, tag, description = self.model.register_component(tag, description)
        print(f'Componente cadastrado -> ID: {self.component_id}, Tag: {tag}, Descrição: {description}')
        self.view.hide()
        self.repairView.update_tag(tag)
        self.repairView.show()

    def register_repairs(self):
        repairs = []
        for i in range(self.repairView.repairTable.rowCount()):
            repair_id = str(uuid.uuid4())
            time_between_fails = self.repairView.repairTable.item(i, 1).text()
            repair_time = self.repairView.repairTable.item(i, 2).text()
            repairs.append({'repair_id': repair_id, 'time_between_fails': time_between_fails, 'repair_time': repair_time, 'component_id': self.component_id})
            print(f'Reparo cadastrado -> ID: {repair_id}, tempo entre falhas: {time_between_fails}, Tempo de reparo: {repair_time} componente: {self.component_id}')
        self.model.register_repairs(repairs)