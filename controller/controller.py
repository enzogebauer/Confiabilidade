from model import Model
from view.view import View
from view.repair_view import RepairView
from view.aderency_view import AderencyView
import uuid
from PyQt5.QtWidgets import QMessageBox
from .testeDeAderenciaFinal import (
    compare_distributions,
    calculate_time_weibull,
    calculate_time_lognormal,
)


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
        self.aderency_view.realizeAnalysis.clicked.connect(
            self.calculate_time_from_confidence
        )
        self.best_distribution = None
        self.alpha = None
        self.beta = None
        self.mu = None
        self.sigma = None
        self.tbf_unit = None

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
        time_between_fails, self.tbf_unit = self.model.select_tbf_data(
            self.get_component_id()
        )

        # Verificar se há dados de tempo entre falhas
        if not time_between_fails:
            print("Não há dados de tempo entre falhas para o componente.")
            return

        # Verificar se a unidade de tempo está presente
        if self.tbf_unit is None:
            print("Não há unidade de tempo entre falhas disponível.")
            return

        print("TIME BETWEEN FAILS:", time_between_fails, "TBF UNIT:", self.tbf_unit)

        fail_times = [float(time) for time in time_between_fails]
        dist, self.best_distribution = compare_distributions(fail_times, self.tbf_unit)
        if self.best_distribution == "Weibull":
            self.alpha = dist.alpha
            self.beta = dist.beta
            print("alpha: ", self.alpha, " beta: ", self.beta)
            self.aderency_view.display_image(
                "best_distribution.png",
                f"Gráfico da Melhor Distribuição: Weibull, CI: 90%, α: {self.alpha:.2f}, β: {self.beta:.2f}",
            )
        else:
            self.mu = dist.mu
            self.sigma = dist.sigma
            self.aderency_view.display_image(
                "best_distribution.png",
                f"Gráfico da Melhor Distribuição: Lognormal, CI: 90%, μ: {self.mu:.2f}, σ: {self.sigma:.2f}",
            )
        print(f"A distribuição com maior aderência é: {self.best_distribution}")

    def calculate_time_from_confidence(self):
        confidence_text = self.aderency_view.inputBox.text()
        if confidence_text.endswith("%"):
            confidence_text = confidence_text[:-1]  # Remove the '%' symbol
        confidence = float(confidence_text)
        confidence = confidence / 100

        if self.best_distribution == "Weibull":
            print(
                "Calculando tempo correspondente para Weibull com os parametros alpha ",
                self.alpha,
                " e beta ",
                self.beta,
                " e confiança ",
                confidence,
            )
            time_for_reliability = calculate_time_weibull(
                self.alpha, self.beta, confidence
            )
        else:
            print(
                "Calculando tempo correspondente para Lognormal com os parametros mu ",
                self.mu,
                " e sigma ",
                self.sigma,
                " e confiança ",
                confidence,
            )
            time_for_reliability = calculate_time_lognormal(
                self.mu, self.sigma, confidence
            )

        self.aderency_view.responseOutput.setText(
            f"Tempo correspondente: {time_for_reliability:.2f} {self.tbf_unit}"
        )
        print(f"Tempo correspondente: {time_for_reliability:.2f} {self.tbf_unit}")
