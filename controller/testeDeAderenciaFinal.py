import numpy as np
import matplotlib.pyplot as plt
from reliability.Fitters import Fit_Weibull_2P, Fit_Gamma_2P, Fit_Lognormal_2P
from scipy.stats import norm

def calculate_r_squared(observed, predicted):
    """
    Calcula o coeficiente de determinação (R²) entre os valores observados e previstos.
    """
    ss_residual = np.sum((observed - predicted)**2)
    ss_total = np.sum((observed - np.mean(observed))**2)
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
    mse = np.mean((observed - predicted)**2)
    return mse

def compare_distributions(fail_times):
    """
    Compara as distribuições Weibull, Gamma e Lognormal com base nas métricas (R², MAE e MSE)
    e retorna a distribuição que apresenta a maior aderência aos dados.
    """
    # Ajustar distribuição Weibull de 2 parâmetros
    wb = Fit_Weibull_2P(fail_times)

    # Ajustar distribuição Lognormal de 2 parâmetros
    lognorm = Fit_Lognormal_2P(fail_times)

    # Calcular valores previstos para cada distribuição
    predicted_wb = wb.distribution.CDF(fail_times)
    predicted_lognorm = norm.cdf(np.log(fail_times), loc=lognorm.mu, scale=lognorm.sigma)

    # Calcular métricas para distribuição Weibull
    r_squared_wb = calculate_r_squared(np.sort(fail_times), predicted_wb)
    mae_wb = calculate_mae(np.sort(fail_times), predicted_wb)
    mse_wb = calculate_mse(np.sort(fail_times), predicted_wb)


    # Calcular métricas para distribuição Lognormal
    r_squared_lognorm = calculate_r_squared(np.sort(fail_times), predicted_lognorm)
    mae_lognorm = calculate_mae(np.sort(fail_times), predicted_lognorm)
    mse_lognorm = calculate_mse(np.sort(fail_times), predicted_lognorm)

    # Exibir as métricas calculadas para cada distribuição
    print(f"Weibull - R²: {r_squared_wb}, MAE: {mae_wb}, MSE: {mse_wb}")
    print(f"Lognormal - R²: {r_squared_lognorm}, MAE: {mae_lognorm}, MSE: {mse_lognorm}")

    # Comparar as métricas e determinar a distribuição com maior aderência
    metrics = {
        'Weibull': (r_squared_wb, mae_wb, mse_wb),
        'Lognormal': (r_squared_lognorm, mae_lognorm, mse_lognorm)
    }

    # Identificar a distribuição com a maior aderência (maior R²)
    best_distribution = max(metrics, key=lambda k: metrics[k][0])
    
    # Plotar o gráfico de confiabilidade para a distribuição escolhida
    plot_reliability(fail_times, 'Weibull', 'weibull_reliability.png')
    plot_reliability(fail_times, 'Lognormal', 'lognormal_reliability.png')

    return best_distribution

def plot_reliability(fail_times, distribution, filename):
    """
    Plota o gráfico de confiabilidade para a distribuição escolhida.

    A confiabilidade é calculada como 1 - CDF (função de distribuição acumulada).
    """
    if distribution == 'Weibull':
        dist = Fit_Weibull_2P(fail_times).distribution
    elif distribution == 'Lognormal':
        dist = Fit_Lognormal_2P(fail_times).distribution
    else:
        raise ValueError("Distribuição inválida. Escolha entre 'Weibull' ou 'Lognormal'.")

    times = np.linspace(min(fail_times), max(fail_times), 1000)
    reliability = 1 - dist.CDF(times)
    
    plt.figure(figsize=(8, 6))
    plt.plot(times, reliability, label=distribution)
    plt.xlabel('Tempo')
    plt.ylabel('Confiabilidade')
    plt.title(f'Gráfico de Confiabilidade para Distribuição {distribution}')
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)

# Lista de tempos de falha
fail_times = [24, 38, 56, 85, 122, 157, 240, 470, 680, 930, 1320, 1655]

# Comparar as distribuições e obter a distribuição com maior aderência
best_fit = compare_distributions(fail_times)
print(f"A distribuição com maior aderência é: {best_fit}")
