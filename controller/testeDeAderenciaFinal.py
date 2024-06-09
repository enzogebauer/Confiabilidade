import numpy as np
import matplotlib.pyplot as plt
from reliability.Fitters import Fit_Weibull_2P, Fit_Lognormal_2P
from scipy.stats import norm
from scipy.stats import weibull_min


def calculate_time_weibull(alpha, beta, reliability_min):
    """
    Calcula o tempo até que a confiabilidade caia para um determinado valor na distribuição Weibull.

    Parâmetros:
    - alpha: Parâmetro de escala da distribuição Weibull.
    - beta: Parâmetro de forma da distribuição Weibull.
    - reliability_min: Confiança mínima desejada (0 < reliability_min < 1), onde reliability_min é o valor de confiabilidade que queremos alcançar.

    Retorna:
    - Tempo correspondente para a confiabilidade dada.
    """
    # Calcula o tempo correspondente na distribuição Weibull
    time = alpha * (-np.log(reliability_min)) ** (1 / beta)

    return time


def calculate_time_lognormal(mu, sigma, reliability_min):
    print(reliability_min)
    z = norm.ppf(1 - reliability_min)
    return np.exp(mu + sigma * z)


def calculate_r_squared(observed, predicted):
    """
    Calcula o coeficiente de determinação (R²) entre os valores observados e previstos.
    """
    ss_residual = np.sum((observed - predicted) ** 2)
    ss_total = np.sum((observed - np.mean(observed)) ** 2)
    r_squared = 1 - (ss_residual / ss_total)
    return r_squared


def calculate_mae(observed, predicted):
    """
    Calcula o erro médio absoluto (MAE) entre os valores observados e previstos.
    """
    mae = np.mean(np.abs(observed - predicted))
    return mae


def calculate_mse(observed, predicted):
    """
    Calcula o erro quadrático médio (MSE) entre os valores observados e previstos.
    """
    mse = np.mean((observed - predicted) ** 2)
    return mse


def compare_distributions(fail_times, tbf_unit):
    """
    Compara as distribuições Weibull e Lognormal com base em uma pontuação combinada das métricas (R², MAE e MSE)
    e retorna a distribuição que apresenta a maior aderência aos dados.
    """
    # Ajustar distribuição Weibull de 2 parâmetros
    wb = Fit_Weibull_2P(fail_times)

    # Ajustar distribuição Lognormal de 2 parâmetros
    lognorm = Fit_Lognormal_2P(fail_times)

    # Calcular valores previstos para cada distribuição
    predicted_wb = wb.distribution.CDF(fail_times)
    predicted_lognorm = norm.cdf(
        np.log(fail_times), loc=lognorm.mu, scale=lognorm.sigma
    )

    # Calcular métricas para distribuição Weibull
    r_squared_wb = calculate_r_squared(np.sort(fail_times), predicted_wb)
    mae_wb = calculate_mae(np.sort(fail_times), predicted_wb)
    mse_wb = calculate_mse(np.sort(fail_times), predicted_wb)

    # Calcular métricas para distribuição Lognormal
    r_squared_lognorm = calculate_r_squared(np.sort(fail_times), predicted_lognorm)
    mae_lognorm = calculate_mae(np.sort(fail_times), predicted_lognorm)
    mse_lognorm = calculate_mse(np.sort(fail_times), predicted_lognorm)

    # Normalizar MAE e MSE (inverter para que maior seja melhor)
    max_mae = max(mae_wb, mae_lognorm)
    max_mse = max(mse_wb, mse_lognorm)
    norm_mae_wb = 1 / (mae_wb / max_mae)
    norm_mae_lognorm = 1 / (mae_lognorm / max_mae)
    norm_mse_wb = 1 / (mse_wb / max_mse)
    norm_mse_lognorm = 1 / (mse_lognorm / max_mse)

    # Calcular pontuação combinada para cada distribuição (assumindo pesos iguais)
    score_wb = (r_squared_wb + norm_mae_wb + norm_mse_wb) / 3
    score_lognorm = (r_squared_lognorm + norm_mae_lognorm + norm_mse_lognorm) / 3

    # Determinar a melhor distribuição com base na pontuação
    best_distribution = "Weibull" if score_wb > score_lognorm else "Lognormal"
    print(
        f"A distribuição com maior aderência é: {best_distribution} (Weibull: {score_wb}, Lognormal: {score_lognorm})"
    )

    # Plotar o gráfico de confiabilidade para a distribuição escolhida
    if best_distribution == "Weibull":
        dist = Fit_Weibull_2P(
            failures=fail_times,
            right_censored=None,
            show_probability_plot=None,
            print_results=None,
            CI=0.90,
            quantiles=None,
            CI_type="time",
            method="MLE",
            optimizer=None,
            force_beta=None,
            downsample_scatterplot=True,
        )
    else:
        dist = Fit_Lognormal_2P(
            failures=fail_times,
            right_censored=None,
            show_probability_plot=None,
            print_results=None,
            CI=0.90,
            quantiles=None,
            optimizer=None,
            CI_type="time",
            method="MLE",
            force_sigma=None,
            downsample_scatterplot=None,
        )

    times = np.linspace(min(fail_times), max(fail_times), 1000)
    reliability = 1 - dist.distribution.CDF(times)

    plt.figure(figsize=(8, 6))
    plt.plot(times, reliability, label=best_distribution)
    plt.xlabel(f"Tempo ({tbf_unit})")
    plt.ylabel("Confiabilidade em decimal com valores de 0 a 1")
    plt.title(f"Gráfico de Confiabilidade para Distribuição {best_distribution}")
    plt.savefig("best_distribution.png")

    return dist, best_distribution
