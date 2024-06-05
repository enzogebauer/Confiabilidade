from model import Model
from view.view import View
from view.repair_view import RepairView
from view.aderency_view import AderencyView
import uuid
from PyQt5.QtWidgets import QMessageBox
from .testeDeAderenciaFinal import compare_distributions


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.repairView = RepairView()
        self.view.button.clicked.connect(self.register_component)
        self.repairView.saveRepairsButton.clicked.connect(self.register_repairs)
        self.view.show()
        self.aderency_view = AderencyView()
        self.aderency_view.shown.connect(self.run_test_and_show_results)

    def get_component_id(self):
        return self.component_id

    def register_component(self):
        tag = self.view.tagInputBox.text()
        description = self.view.descInputBox.text()
        self.component_id, tag, description = self.model.register_component(
            tag, description
        )
        print(
            f"Componente cadastrado -> ID: {self.component_id}, Tag: {tag}, Descrição: {description}"
        )
        self.view.hide()
        self.repairView.update_tag(tag)
        self.repairView.show()

    def register_repairs(self):
        reply = QMessageBox.question(
            self.repairView,
            "Confirmação",
            "Você tem certeza que deseja salvar os reparos?\nEssa ação é única e irreversível.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            repairs = []
            for i in range(self.repairView.repairTable.rowCount()):
                repair_id = str(uuid.uuid4())
                time_between_fails = self.repairView.repairTable.item(i, 1).text()
                tbf_unit = self.repairView.repairTable.item(i, 2).text()
                repair_time = self.repairView.repairTable.item(i, 3).text()
                rt_unit = self.repairView.repairTable.item(i, 4).text()
                repairs.append(
                    {
                        "repair_id": repair_id,
                        "time_between_fails": time_between_fails,
                        "repair_time": repair_time,
                        "component_id": self.component_id,
                        "tbf_unit": tbf_unit,
                        "rt_unit": rt_unit,
                    }
                )
                print(
                    f"Reparo cadastrado -> ID: {repair_id}, tempo entre falhas: {time_between_fails} {tbf_unit}, Tempo de reparo: {repair_time} {rt_unit}, componente: {self.component_id}"
                )
            self.repairView.hide()
            self.model.register_repairs(repairs)
            self.aderency_view.show()

    def run_test_and_show_results(self):
        time_between_fails, tbf_unit = self.model.select_tbf_data(
            self.get_component_id()
        )

        # Verificar se há dados de tempo entre falhas
        if not time_between_fails:
            print("Não há dados de tempo entre falhas para o componente.")
            return

        # Verificar se a unidade de tempo está presente
        if tbf_unit is None:
            print("Não há unidade de tempo entre falhas disponível.")
            return

        print("TIME BETWEEN FAILS:", time_between_fails, "TBF UNIT:", tbf_unit)

        fail_times = [float(time) for time in time_between_fails]
        dist, best_distribution = compare_distributions(fail_times, tbf_unit)
        if best_distribution == "Weibull":
            p1 = dist.alpha
            p2 = dist.beta
            self.aderency_view.display_image(
                "best_distribution.png",
                f"Gráfico da Melhor Distribuição: Weibull, CI: 90%, α: {p1:.2f}, β: {p2:.2f}",
            )
        else:
            p1 = dist.mu
            p2 = dist.sigma
            self.aderency_view.display_image(
                "best_distribution.png",
                f"Gráfico da Melhor Distribuição: Lognormal, CI: 90%, μ: {p1:.2f}, σ: {p2:.2f}",
            )
        print(f"A distribuição com maior aderência é: {best_distribution}")
