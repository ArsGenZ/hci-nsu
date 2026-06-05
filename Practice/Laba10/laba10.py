import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

warnings.filterwarnings("ignore")


# ==========================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================================
def computeCost(X, y, theta):
    """Вычисляет MSE (Mean Squared Error)"""
    m = len(y)
    predictions = X.dot(theta)
    sq_errors = (predictions - y) ** 2
    return (1 / (2 * m)) * np.sum(sq_errors)


def gradientDescent(X, y, theta, alpha, num_iters):
    """Градиентный спуск с сохранением истории функции потерь"""
    m = len(y)
    J_history = []

    for i in range(num_iters):
        error = X.dot(theta) - y
        theta -= (alpha / m) * X.T.dot(error)
        J_history.append(computeCost(X, y, theta))

    return theta, J_history


# ==========================================
# ЗАДАНИЕ 1: Исследование параметров GD (data1.txt)
# ==========================================
print("=" * 50)
print("ЗАДАНИЕ 1: data1.txt - Градиентный спуск")
print("=" * 50)

if os.path.exists("data1.txt"):
    data = pd.read_csv("data1.txt", header=None)
    X_raw = data[0].values
    y = data[1].values
    m = len(y)

    mu = X_raw.mean()
    sigma = X_raw.std()
    X_norm = (X_raw - mu) / sigma
    X_b = np.vstack([np.ones(m), X_norm]).T

    # 1.1. Разные learning rate
    print("\nГрафик изменения функции потерь при разных learning rate...")
    alphas = [0.001, 0.01, 0.1]
    plt.figure(figsize=(12, 4))
    for i, alpha in enumerate(alphas, 1):
        theta_init = np.zeros(2)
        _, J_hist = gradientDescent(X_b, y, theta_init, alpha, 1500)
        plt.subplot(1, 3, i)
        plt.plot(
            J_hist,
            color="blue" if alpha == 0.01 else "green" if alpha == 0.001 else "red",
        )
        plt.title(f"Alpha = {alpha}")
        plt.xlabel("Iterations")
        plt.ylabel("Cost J")
        plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 1.2. Разное число итераций
    print("\nВлияние числа итераций на аппроксимацию...")
    iterations_list = [100, 500, 1500]
    plt.figure(figsize=(12, 4))
    for i, iters in enumerate(iterations_list, 1):
        theta_init = np.zeros(2)
        theta, _ = gradientDescent(X_b, y, theta_init, 0.01, iters)

        y_pred = X_b.dot(theta)
        sort_idx = np.argsort(X_raw)

        plt.subplot(1, 3, i)
        plt.scatter(X_raw, y, marker="x", c="r")
        plt.plot(X_raw[sort_idx], y_pred[sort_idx], "b-")
        plt.title(f"Iter = {iters}")
        plt.xlabel("Population")
        plt.ylabel("Profit")
        plt.grid(True)
    plt.tight_layout()
    plt.show()

else:
    print("Файл 'data1.txt' не найден. Положите его в папку со скриптом.")

# ==========================================
# ЗАДАНИЕ 2: Применение к Salary_Data.xls
# ==========================================
print("\n" + "=" * 50)
print("ЗАДАНИЕ 2: Salary_Data.xls - Полный цикл обучения")
print("=" * 50)

try:
    salary_data = pd.read_excel("Salary_Data.xls")
    X_sal = salary_data["YearsExperience"].values.reshape(-1, 1)
    y_sal = salary_data["Salary"].values
    m_sal = len(y_sal)

    # 2.1. Зависимость зарплаты от стажа
    plt.figure(figsize=(7, 5))
    plt.scatter(X_sal, y_sal, c="blue", alpha=0.7)
    plt.xlabel("YearsExperience")
    plt.ylabel("Salary")
    plt.title("Salary vs Years of Experience")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()

    # Подготовка к GD
    mu_sal = X_sal.mean()
    sigma_sal = X_sal.std()
    X_sal_norm = (X_sal - mu_sal) / sigma_sal
    X_sal_b = np.vstack([np.ones(m_sal), X_sal_norm.ravel()]).T

    theta_sal, J_hist_sal = gradientDescent(X_sal_b, y_sal, np.zeros(2), 0.01, 1000)

    print(f"GD обучен: theta0={theta_sal[0]:.2f}, theta1={theta_sal[1]:.2f}")

    # 2.2. График функции ошибки
    plt.figure(figsize=(7, 5))
    plt.plot(J_hist_sal, color="purple")
    plt.xlabel("Number of iterations")
    plt.ylabel("Cost J")
    plt.title("Cost function convergence")
    plt.grid(True)
    plt.show()

    # 2.3. Результат обучения (линия регрессии)
    y_sal_pred = X_sal_b.dot(theta_sal)
    sort_idx_sal = np.argsort(X_sal.ravel())

    plt.figure(figsize=(7, 5))
    plt.scatter(X_sal, y_sal, c="blue", alpha=0.7, label="Actual")
    plt.plot(
        X_sal[sort_idx_sal],
        y_sal_pred[sort_idx_sal],
        "r-",
        linewidth=2,
        label="Predicted",
    )
    plt.xlabel("YearsExperience")
    plt.ylabel("Salary")
    plt.title("Linear Regression on Salary Data (Gradient Descent)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()

    # 2.4. Контурная карта параметров theta0 и theta1
    print("Построение контурной карты...")
    theta0_vals = np.linspace(theta_sal[0] - 2000, theta_sal[0] + 2000, 100)
    theta1_vals = np.linspace(theta_sal[1] - 5000, theta_sal[1] + 5000, 100)
    J_vals = np.zeros((len(theta0_vals), len(theta1_vals)))

    for i, t0 in enumerate(theta0_vals):
        for j, t1 in enumerate(theta1_vals):
            J_vals[i, j] = computeCost(X_sal_b, y_sal, np.array([t0, t1]))
    J_vals = J_vals.T

    # # Безопасные уровни для log-масштаба
    # min_log = np.log10(np.max(J_vals) * 1e-4)
    # max_log = np.log10(np.max(J_vals) * 0.5)

    plt.figure(figsize=(8, 6))
    plt.contour(theta0_vals, theta1_vals, J_vals, levels=np.logspace(-2, 20, 200))
    plt.plot(
        theta_sal[0],
        theta_sal[1],
        "rx",
        markersize=12,
        markeredgewidth=3,
        label="Optimal theta",
    )
    plt.xlabel("theta0 (intercept)")
    plt.ylabel("theta1 (slope)")
    plt.title("Contour plot of Cost Function")
    plt.legend()
    plt.grid(True)
    plt.show()
    # Красный крест показывает минимум функции потерь, к которому сошелся градиентный спуск.
except FileNotFoundError:
    print("Файл 'Salary_Data.xls' не найден.")
except Exception as e:
    print(f"Ошибка в Задании 2: {e}")

# ==========================================
# ЗАДАНИЕ 3: Решение через scikit-learn
# ==========================================
print("\n" + "=" * 50)
print("ЗАДАНИЕ 3: scikit-learn на Salary_Data.xls")
print("=" * 50)

try:
    if "X_sal" in locals():
        model = LinearRegression()
        model.fit(X_sal, y_sal)
        y_pred_sk = model.predict(X_sal)

        mse = mean_squared_error(y_sal, y_pred_sk)
        r2 = r2_score(y_sal, y_pred_sk)

        print(f"sklearn параметры:")
        print(f"   theta0 (intercept): {model.intercept_:.2f}")
        print(f"   theta1 (coef)     : {model.coef_[0]:.2f}")
        print(f"   MSE: {mse:.2f}")
        print(f"   R2 : {r2:.4f}")

        plt.figure(figsize=(7, 5))
        plt.scatter(X_sal, y_sal, c="blue", alpha=0.7, label="Actual")
        plt.plot(
            X_sal[sort_idx_sal],
            y_pred_sk[sort_idx_sal],
            "g-",
            linewidth=2,
            label="sklearn Predicted",
        )
        plt.xlabel("YearsExperience")
        plt.ylabel("Salary")
        plt.title("Linear Regression with scikit-learn")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.show()
    else:
        print("Пропуск Задания 3: данные Salary_Data не были загружены.")
except Exception as e:
    print(f"Ошибка в Задании 3: {e}")

print("\nЛабораторная работа 10 успешно завершена.")
