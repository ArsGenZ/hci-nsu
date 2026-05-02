import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score, auc, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, label_binarize

print("=" * 80)
print("ЛАБОРАТОРНАЯ РАБОТА 9: МЕТРИКИ ОБУЧЕНИЯ (ПОЛНОЕ РЕШЕНИЕ)")
print("=" * 80)

# ============================================================================
# ЗАДАЧА 1: Расчет метрик по заданным значениям
# ============================================================================
print("\n" + "=" * 80)
print("ЗАДАЧА 1: Расчет метрик классификации")
print("=" * 80)

TP, FP, TN, FN = 80, 15, 50, 10

accuracy = (TP + TN) / (TP + TN + FP + FN)
precision = TP / (TP + FP) if (TP + FP) != 0 else 0
recall = TP / (TP + FN) if (TP + FN) != 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

print(f"Accuracy (Точность): {accuracy:.4f}")
print(f"Precision (Точность положительного класса): {precision:.4f}")
print(f"Recall (Полнота): {recall:.4f}")
print(f"F1-score: {f1:.4f}")

# ============================================================================
# ЗАДАЧА 2: TPR, FPR и ROC-AUC для двух моделей
# ============================================================================
print("\n" + "=" * 80)
print("ЗАДАЧА 2: TPR, FPR и ROC-AUC")
print("=" * 80)

y_true = np.array([0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1])
y_pred1 = np.array(
    [
        0.1,
        0.4,
        0.35,
        0.8,
        0.7,
        0.9,
        0.2,
        0.95,
        0.3,
        0.85,
        0.78,
        0.4,
        0.6,
        0.7,
        0.5,
        0.88,
    ]
)
y_pred2 = np.array(
    [
        0.05,
        0.25,
        0.1,
        0.9,
        0.4,
        0.88,
        0.3,
        0.92,
        0.15,
        0.75,
        0.65,
        0.35,
        0.55,
        0.8,
        0.45,
        0.85,
    ]
)


def calc_metrics(y_true, y_pred, threshold):
    y_bin = (y_pred >= threshold).astype(int)
    tp = np.sum((y_true == 1) & (y_bin == 1))
    fp = np.sum((y_true == 0) & (y_bin == 1))
    fn = np.sum((y_true == 1) & (y_bin == 0))
    tn = np.sum((y_true == 0) & (y_bin == 0))
    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    return tpr, fpr


print(f"{'Model':<8} | {'Thresh':<6} | TPR | FPR")
print("-" * 30)
for name, y_p in [("Model 1", y_pred1), ("Model 2", y_pred2)]:
    for t in [0.5, 0.8]:
        tpr, fpr = calc_metrics(y_true, y_p, t)
        print(f"{name:<8} | {t:<6.1f} | {tpr:.2f} | {fpr:.2f}")

# Построение ROC-AUC кривой
fpr1, tpr1, _ = roc_curve(y_true, y_pred1)
fpr2, tpr2, _ = roc_curve(y_true, y_pred2)
auc1 = auc(fpr1, tpr1)
auc2 = auc(fpr2, tpr2)

plt.figure(figsize=(6, 5))
plt.plot(fpr1, tpr1, label=f"Model 1 (AUC = {auc1:.2f})", marker="o")
plt.plot(fpr2, tpr2, label=f"Model 2 (AUC = {auc2:.2f})", marker="s")
plt.plot([0, 1], [0, 1], "k--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve (Task 2)")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# ============================================================================
# ЗАДАЧА 3: Классификация цифр с улучшениями
# ============================================================================
print("\n" + "=" * 80)
print("ЗАДАЧА 3: Классификация цифр (Сравнение улучшений)")
print("=" * 80)

digits = load_digits()
X_train, X_test, y_train, y_test = train_test_split(
    digits.data, digits.target, test_size=0.3, random_state=60
)

# Масштабирование данных (критически важно для нейросетей)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# --- Функция для расчета Macro Average ROC-AUC ---
def calculate_macro_auc(y_true, y_score):
    fpr, tpr, roc_auc = {}, {}, {}
    n_classes = y_score.shape[1]

    # 1. Бинаризуем метки для корректного расчёта микро-усреднения
    y_true_bin = label_binarize(y_true, classes=range(n_classes))

    # 2. Расчёт для каждого класса
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # 3. Micro-average
    fpr["micro"], tpr["micro"], _ = roc_curve(y_true_bin.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    # 4. Macro-average
    all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))
    mean_tpr = np.zeros_like(all_fpr)

    for i in range(n_classes):
        mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])

    mean_tpr /= n_classes
    fpr["macro"] = all_fpr
    tpr["macro"] = mean_tpr
    roc_auc["macro"] = auc(all_fpr, mean_tpr)

    return fpr, tpr, roc_auc


# 1. Базовая модель (Простая архитектура)
print("\n1. Базовая модель (Слой: 32)")
model_base = MLPClassifier(hidden_layer_sizes=(32,), max_iter=500, random_state=42)
model_base.fit(X_train, y_train)
y_score_base = model_base.predict_proba(X_test)
acc_base = accuracy_score(y_test, model_base.predict(X_test))
print(f"Accuracy: {acc_base:.4f}")

# 2. Улучшение 1: Усложнение архитектуры (Больше слоев и нейронов)
# Цель: Увеличить емкость модели для изучения более сложных паттернов.
print("\n2. Улучшение 2: Усложнение архитектуры (Слои: 100, 50, 20)")
model_v2 = MLPClassifier(
    hidden_layer_sizes=(100, 50, 20), activation="relu", max_iter=500, random_state=42
)
model_v2.fit(X_train, y_train)
y_score_v2 = model_v2.predict_proba(X_test)
acc_v2 = accuracy_score(y_test, model_v2.predict(X_test))
print(f"Accuracy: {acc_v2:.4f}")

# 3. Улучшение 2: Регуляризация (Добавление L2-регуляризации)
# Цель: Предотвратить переобучение сложной модели, штрафуя за большие веса.
print("\n3. Улучшение 3: Регуляризация (Alpha=0.01)")
model_v3 = MLPClassifier(
    hidden_layer_sizes=(32,), alpha=0.01, max_iter=500, random_state=42
)
model_v3.fit(X_train, y_train)
y_score_v3 = model_v3.predict_proba(X_test)
acc_v3 = accuracy_score(y_test, model_v3.predict(X_test))
print(f"Accuracy: {acc_v3:.4f}")

# 4. Улучшение 3: Смена оптимизатора (Adam)
# Цель: Использовать более адаптивный алгоритм оптимизации для более быстрой и точной сходимости.
print("\n4. Улучшение 4: Оптимизатор Adam")
model_v4 = MLPClassifier(
    hidden_layer_sizes=(32,), solver="adam", max_iter=500, random_state=42
)
model_v4.fit(X_train, y_train)
y_score_v4 = model_v4.predict_proba(X_test)
acc_v4 = accuracy_score(y_test, model_v4.predict(X_test))
print(f"Accuracy: {acc_v4:.4f}")

# --- Построение сравнительного графика ROC-AUC ---
print("\nПостроение ROC-AUC кривых для всех моделей...")

res_base = calculate_macro_auc(y_test, y_score_base)
res_v2 = calculate_macro_auc(y_test, y_score_v2)
res_v3 = calculate_macro_auc(y_test, y_score_v3)
res_v4 = calculate_macro_auc(y_test, y_score_v4)

plt.figure(figsize=(10, 8))

models_data = [
    ("Base Model", res_base, "red"),
    ("Improved Arch (v2)", res_v2, "blue"),
    ("Regularized (v3)", res_v3, "green"),
    ("Adam Solver (v4)", res_v4, "orange"),
]

for name, res, color in models_data:
    fpr, tpr, roc_auc = res
    plt.plot(
        fpr["macro"],
        tpr["macro"],
        label=f"{name} (Macro AUC = {roc_auc['macro']:.3f})",
        color=color,
        lw=2,
    )

plt.plot([0, 1], [0, 1], "k--", lw=1, alpha=0.5)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves Comparison (Task 3 Improvements)")
plt.legend(loc="lower right")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Итоговая таблица
print("\n" + "=" * 80)
print("ИТОГОВОЕ СРАВНЕНИЕ (Macro AUC)")
print("=" * 80)
print(f"Базовая модель:      {res_base[2]['macro']:.4f}")
print(f"Улучшение 2 (Arch):  {res_v2[2]['macro']:.4f}")
print(f"Улучшение 3 (Reg):   {res_v3[2]['macro']:.4f}")
print(f"Улучшение 4 (Adam):  {res_v4[2]['macro']:.4f}")
