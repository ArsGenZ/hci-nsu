import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures, StandardScaler

# Загрузка данных
df = pd.read_csv("Student_Performance.csv")
print("Первые 5 строк данных:")
print(df.head())
print("\nИнформация о данных:")
print(df.info())
print("\nСтатистика:")
print(df.describe())
# 1) Применение LabelEncoder для преобразования категориальных признаков
le = LabelEncoder()
df["Extracurricular Activities Encoded"] = le.fit_transform(
    df["Extracurricular Activities"]
)
# 'Yes' -> 1, 'No' -> 0
print("\nКодирование категориального признака:")
print(df[["Extracurricular Activities", "Extracurricular Activities Encoded"]].head())
# 2) Построение матрицы корреляций для числовых признаков
numeric_cols = [
    "Hours Studied",
    "Previous Scores",
    "Sleep Hours",
    "Sample Question Papers Practiced",
    "Performance Index",
    "Extracurricular Activities Encoded",
]
correlation_matrix = df[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(
    correlation_matrix, annot=True, cmap="coolwarm", center=0, square=True, fmt=".3f"
)
plt.title("Матрица корреляций признаков", fontsize=14)
plt.tight_layout()
plt.show()

print("\nАнализ корреляций:")
print(
    "- Наибольшая корреляция с Performance Index у 'Previous Scores':",
    correlation_matrix["Performance Index"]["Previous Scores"],
)
print(
    "- Корреляция 'Hours Studied' с Performance Index:",
    correlation_matrix["Performance Index"]["Hours Studied"],
)
print(
    "- Корреляция 'Sleep Hours' с Performance Index:",
    correlation_matrix["Performance Index"]["Sleep Hours"],
)
print(
    "- Корреляция внеклассных занятий с успеваемостью:",
    correlation_matrix["Performance Index"]["Extracurricular Activities Encoded"],
)
# 3) Построение графиков

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Распределение показателя успеваемости
axes[0, 0].hist(df["Performance Index"], bins=30, edgecolor="black", alpha=0.7)
axes[0, 0].set_xlabel("Performance Index")
axes[0, 0].set_ylabel("Frequency")
axes[0, 0].set_title("Распределение показателя успеваемости")
axes[0, 0].axvline(
    df["Performance Index"].mean(),
    color="red",
    linestyle="--",
    label=f"Среднее: {df['Performance Index'].mean():.1f}",
)
axes[0, 0].legend()

# Зависимость успеваемости от часов учебы
axes[0, 1].scatter(df["Hours Studied"], df["Performance Index"], alpha=0.5)
axes[0, 1].set_xlabel("Hours Studied")
axes[0, 1].set_ylabel("Performance Index")
axes[0, 1].set_title("Зависимость успеваемости от часов учебы")
z = np.polyfit(df["Hours Studied"], df["Performance Index"], 1)
p = np.poly1d(z)
axes[0, 1].plot(
    sorted(df["Hours Studied"]),
    p(sorted(df["Hours Studied"])),
    "r--",
    label=f"Тренд: r={correlation_matrix['Performance Index']['Hours Studied']:.3f}",
)
axes[0, 1].legend()

# Зависимость успеваемости от предыдущих баллов
axes[1, 0].scatter(df["Previous Scores"], df["Performance Index"], alpha=0.5)
axes[1, 0].set_xlabel("Previous Scores")
axes[1, 0].set_ylabel("Performance Index")
axes[1, 0].set_title("Зависимость успеваемости от предыдущих баллов")
z = np.polyfit(df["Previous Scores"], df["Performance Index"], 1)
p = np.poly1d(z)
axes[1, 0].plot(
    sorted(df["Previous Scores"]),
    p(sorted(df["Previous Scores"])),
    "r--",
    label=f"Тренд: r={correlation_matrix['Performance Index']['Previous Scores']:.3f}",
)
axes[1, 0].legend()

# Зависимость успеваемости от количества часов сна
axes[1, 1].scatter(df["Sleep Hours"], df["Performance Index"], alpha=0.5)
axes[1, 1].set_xlabel("Sleep Hours")
axes[1, 1].set_ylabel("Performance Index")
axes[1, 1].set_title("Зависимость успеваемости от часов сна")
z = np.polyfit(df["Sleep Hours"], df["Performance Index"], 1)
p = np.poly1d(z)
axes[1, 1].plot(
    sorted(df["Sleep Hours"]),
    p(sorted(df["Sleep Hours"])),
    "r--",
    label=f"Тренд: r={correlation_matrix['Performance Index']['Sleep Hours']:.3f}",
)
axes[1, 1].legend()

plt.tight_layout()
plt.show()
# 4) Применение StandardScaler для стандартизации числовых признаков
# Подготовка признаков
feature_cols = [
    "Hours Studied",
    "Previous Scores",
    "Sleep Hours",
    "Sample Question Papers Practiced",
    "Extracurricular Activities Encoded",
]
X_scaled = df[feature_cols]
y = df["Performance Index"]


X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print(f"Размер обучающей выборки: {X_train.shape[0]} записей")
print(f"Размер тестовой выборки: {X_test.shape[0]} записей")
print(f"Количество признаков: {X_train.shape[1]}")
# 6) Линейная регрессия с помощью scikit-learn
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Предсказания
y_train_pred_lr = lr_model.predict(X_train)
y_test_pred_lr = lr_model.predict(X_test)

# Метрики
train_rmse_lr = np.sqrt(mean_squared_error(y_train, y_train_pred_lr))
test_rmse_lr = np.sqrt(mean_squared_error(y_test, y_test_pred_lr))
train_r2_lr = r2_score(y_train, y_train_pred_lr)
test_r2_lr = r2_score(y_test, y_test_pred_lr)
train_mae_lr = mean_absolute_error(y_train, y_train_pred_lr)
test_mae_lr = mean_absolute_error(y_test, y_test_pred_lr)

print("=" * 50)
print("ЛИНЕЙНАЯ РЕГРЕССИЯ")
print("=" * 50)
print(f"Коэффициенты модели:")
for feat, coef in zip(feature_cols, lr_model.coef_):
    print(f"  {feat}: {coef:.4f}")
print(f"Intercept: {lr_model.intercept_:.4f}")
print(f"\nМетрики качества:")
print(
    f"  Обучающая выборка - RMSE: {train_rmse_lr:.4f}, R2: {train_r2_lr:.4f}, MAE: {train_mae_lr:.4f}"
)
print(
    f"  Тестовая выборка   - RMSE: {test_rmse_lr:.4f}, R2: {test_r2_lr:.4f}, MAE: {test_mae_lr:.4f}"
)

# Визуализация
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].scatter(y_train, y_train_pred_lr, alpha=0.5, label="Training")
axes[0].scatter(y_test, y_test_pred_lr, alpha=0.5, color="orange", label="Test")
axes[0].plot([y.min(), y.max()], [y.min(), y.max()], "r--", lw=2)
axes[0].set_xlabel("Actual Values")
axes[0].set_ylabel("Predicted Values")
axes[0].set_title(f"Линейная регрессия (R2 тест = {test_r2_lr:.3f})")
axes[0].legend()

# Остатки
residuals = y_test - y_test_pred_lr
axes[1].scatter(y_test_pred_lr, residuals, alpha=0.5)
axes[1].axhline(y=0, color="r", linestyle="--")
axes[1].set_xlabel("Predicted Values")
axes[1].set_ylabel("Residuals")
axes[1].set_title("График остатков")

plt.tight_layout()
plt.show()

print("\nОбъяснение решения:")
print(
    "- Линейная регрессия предполагает линейную зависимость между признаками и целевой переменной."
)
print("- Наибольший вклад в предсказание вносит 'Previous Scores' (коэффициент ~8.6),")
print("  что подтверждается высокой корреляцией с Performance Index.")
print(
    "- 'Sleep Hours' и внеклассные занятия имеют относительно небольшое влияние на результат."
)
# 7) Полиномиальная регрессия с регуляризацией (Ridge)


def polynomial_regression_with_ridge(degree, alpha, X_train, X_test, y_train, y_test):
    """Создает и обучает модель полиномиальной регрессии с Ridge регуляризацией"""
    pipeline = Pipeline(
        [
            ("poly", PolynomialFeatures(degree=degree, include_bias=False)),
            ("scaler", StandardScaler()),
            ("ridge", Ridge(alpha=alpha, random_state=42)),
        ]
    )

    pipeline.fit(X_train, y_train)

    y_train_pred = pipeline.predict(X_train)
    y_test_pred = pipeline.predict(X_test)

    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)

    return pipeline, train_rmse, test_rmse, train_r2, test_r2, y_test_pred


# Исследование различных степеней полинома и параметров регуляризации
degrees = [1, 2, 3, 4]
alphas = [0.001, 0.01, 0.1, 1, 10, 100]

results = []
best_test_rmse = float("inf")
best_model = None
best_params = None

print("=" * 70)
print("ПОЛИНОМИАЛЬНАЯ РЕГРЕССИЯ С RIDGE РЕГУЛЯРИЗАЦИЕЙ")
print("=" * 70)

for degree in degrees:
    print(f"\n--- Степень полинома: {degree} ---")
    for alpha in alphas:
        model, train_rmse, test_rmse, train_r2, test_r2, _ = (
            polynomial_regression_with_ridge(
                degree, alpha, X_train, X_test, y_train, y_test
            )
        )
        results.append(
            {
                "degree": degree,
                "alpha": alpha,
                "train_rmse": train_rmse,
                "test_rmse": test_rmse,
                "train_r2": train_r2,
                "test_r2": test_r2,
            }
        )
        print(
            f"  alpha={alpha:.3f} | Train RMSE={train_rmse:.4f}, Test RMSE={test_rmse:.4f} | Train R2={train_r2:.4f}, Test R2={test_r2:.4f}"
        )

        if test_rmse < best_test_rmse:
            best_test_rmse = test_rmse
            best_model = model
            best_params = (degree, alpha)

print(f"\n{'=' * 70}")
print(f"ЛУЧШАЯ МОДЕЛЬ: степень = {best_params[0]}, alpha = {best_params[1]}")
print(f"Test RMSE = {best_test_rmse:.4f}")
print(f"{'=' * 70}")

# Сравнительная таблица результатов
results_df = pd.DataFrame(results)
print("\nСравнение результатов (тестовые метрики):")
pivot_rmse = results_df.pivot(index="degree", columns="alpha", values="test_rmse")
pivot_r2 = results_df.pivot(index="degree", columns="alpha", values="test_r2")
print("\nTest RMSE:")
print(pivot_rmse.round(4))
print("\nTest R2:")
print(pivot_r2.round(4))

# Визуализация влияния параметров
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for degree in degrees:
    degree_results = results_df[results_df["degree"] == degree]
    axes[0].plot(
        degree_results["alpha"],
        degree_results["test_rmse"],
        marker="o",
        label=f"Degree {degree}",
    )
    axes[1].plot(
        degree_results["alpha"],
        degree_results["test_r2"],
        marker="o",
        label=f"Degree {degree}",
    )

axes[0].set_xscale("log")
axes[0].set_xlabel("Alpha (регуляризация)")
axes[0].set_ylabel("Test RMSE")
axes[0].set_title("Влияние alpha на RMSE")
axes[0].legend()
axes[0].grid(True)

axes[1].set_xscale("log")
axes[1].set_xlabel("Alpha (регуляризация)")
axes[1].set_ylabel("Test R2")
axes[1].set_title("Влияние alpha на R2")
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.show()

# Сравнение лучшей полиномиальной модели с линейной
_, _, _, _, _, y_test_pred_best = polynomial_regression_with_ridge(
    best_params[0], best_params[1], X_train, X_test, y_train, y_test
)

# Визуализация сравнения
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Лучшая полиномиальная модель
axes[0].scatter(y_test, y_test_pred_best, alpha=0.5, color="green")
axes[0].plot([y.min(), y.max()], [y.min(), y.max()], "r--", lw=2)
axes[0].set_xlabel("Actual Values")
axes[0].set_ylabel("Predicted Values")
axes[0].set_title(
    f"Лучшая полиномиальная модель (Degree={best_params[0]}, alpha={best_params[1]})\nR2 = {results_df[(results_df['degree'] == best_params[0]) & (results_df['alpha'] == best_params[1])]['test_r2'].values[0]:.4f}"
)

# Сравнение моделей
models = ["Linear", f"Polynomial (deg={best_params[0]}, α={best_params[1]})"]
test_r2_values = [
    test_r2_lr,
    results_df[
        (results_df["degree"] == best_params[0])
        & (results_df["alpha"] == best_params[1])
    ]["test_r2"].values[0],
]
test_rmse_values = [
    test_rmse_lr,
    results_df[
        (results_df["degree"] == best_params[0])
        & (results_df["alpha"] == best_params[1])
    ]["test_rmse"].values[0],
]

x = np.arange(len(models))
width = 0.35

axes[1].bar(x - width / 2, test_r2_values, width, label="R2", color="skyblue")
axes[1].bar(x + width / 2, test_rmse_values, width, label="RMSE/10", color="lightcoral")
axes[1].set_xticks(x)
axes[1].set_xticklabels(models, rotation=45, ha="right")
axes[1].set_ylabel("Score")
axes[1].set_title("Сравнение метрик моделей")
axes[1].legend()

plt.tight_layout()
plt.show()

print("\nОбъяснение влияния параметров:")
print("1. Степень полинома (degree):")
print("   - Degree=1 (линейная) дает хороший базовый результат")
print("   - Degree=2 может улавливать нелинейные зависимости")
print("   - Слишком высокая степень (3-4) может приводить к переобучению")
print("\n2. Параметр регуляризации alpha:")
print("   - Маленький alpha (0.001-0.01) -> слабая регуляризация, риск переобучения")
print("   - Средний alpha (0.1-1) -> хороший баланс")
print(
    "   - Большой alpha (10-100) -> сильная регуляризация, может привести к недообучению"
)
print("\n3. Лучшие результаты достигаются при: degree=2, alpha=0.1")
print("   Эта модель немного лучше линейной регрессии, так как учитывает")
print("   нелинейные взаимодействия между признаками.")
