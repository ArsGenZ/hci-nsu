import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")

# Настройка стиля графиков
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["font.size"] = 10


# 1. Загрузка и базовая очистка данных
df = pd.read_csv("titanic.csv")
df = df[["Survived", "Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]]

# Обработка пропусков
df["Age"].fillna(df["Age"].median(), inplace=True)
df["Fare"].fillna(df["Fare"].median(), inplace=True)
df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)


# 2. LabelEncoder для категориальных признаков
df_encoded = df.copy()  # Копия для кодирования
le_sex = LabelEncoder()
le_emb = LabelEncoder()

df_encoded["Sex"] = le_sex.fit_transform(df_encoded["Sex"])  # male=1, female=0
df_encoded["Embarked"] = le_emb.fit_transform(df_encoded["Embarked"])  # C=0, Q=1, S=2

print("Кодирование категориальных признаков:")
print(f"Sex: {dict(zip(le_sex.classes_, le_sex.transform(le_sex.classes_)))}")
print(f"Embarked: {dict(zip(le_emb.classes_, le_emb.transform(le_emb.classes_)))}\n")


# 3. Матрица корреляций
corr_matrix = df_encoded.corr()

# Тепловая карта корреляций
plt.figure(figsize=(9, 7))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0,
    square=True,
    linewidths=1,
    cbar_kws={"shrink": 0.8},
)
plt.title("Матрица корреляций (после LabelEncoder)", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()

# Корреляция с целевой переменной
print("Корреляция признаков с Survived:")
print(corr_matrix["Survived"].drop("Survived").sort_values(ascending=False), "\n")

# Бар-чарт корреляций с Survived
corr_with_target = corr_matrix["Survived"].drop("Survived").sort_values(ascending=False)
plt.figure(figsize=(8, 5))
colors = ["salmon" if v < 0 else "skyblue" for v in corr_with_target.values]
bars = plt.barh(
    corr_with_target.index, corr_with_target.values, color=colors, edgecolor="black"
)
plt.axvline(0, color="gray", linestyle="--", linewidth=0.5)
plt.xlabel("Коэффициент корреляции Пирсона")
plt.title("Влияние признаков на выживаемость", fontsize=14, fontweight="bold")
plt.gca().invert_yaxis()
for bar in bars:
    width = bar.get_width()
    plt.text(
        width + 0.015,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.2f}",
        va="center",
        fontsize=9,
    )
plt.tight_layout()
plt.show()


# 4. Подготовка X и y для моделей (на основе df_encoded)

X = df_encoded.drop("Survived", axis=1)
y = df_encoded["Survived"]


# 5. StandardScaler для числовых признаков

num_cols = ["Pclass", "Age", "SibSp", "Parch", "Fare"]
scaler = StandardScaler()
X_scaled = X.copy()
X_scaled[num_cols] = scaler.fit_transform(X[num_cols])


# 6. Разделение на обучающую и тестовую выборки

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)


# 7. Вспомогательная функция оценки + визуализация


def evaluate(name, model, X_train, X_test, y_train, y_test, plot_cm=True):
    model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    print(f"\n[{name}]")
    print(
        f"Train Acc: {accuracy_score(y_train, y_train_pred):.4f} | Test Acc: {accuracy_score(y_test, y_test_pred):.4f}"
    )
    print(classification_report(y_test, y_test_pred, zero_division=0))
    return model


# 8. KNN + GridSearchCV + Feature Importance

knn = KNeighborsClassifier()
knn_model = evaluate("KNN", knn, X_train, X_test, y_train, y_test)

knn_params = {
    "n_neighbors": [3, 5, 7, 9, 11],
    "weights": ["uniform", "distance"],
    "metric": ["euclidean", "manhattan"],
}
knn_grid = GridSearchCV(KNeighborsClassifier(), knn_params, cv=5, scoring="accuracy")
knn_grid.fit(X_train, y_train)
print(f"\nBest KNN: {knn_grid.best_params_} | CV Score: {knn_grid.best_score_:.4f}")
best_knn = knn_grid.best_estimator_

# Permutation Importance для KNN
perm_knn = permutation_importance(
    best_knn, X_test, y_test, n_repeats=10, random_state=42
)
knn_imp = sorted(
    zip(X.columns, perm_knn.importances_mean), key=lambda x: x[1], reverse=True
)

plt.figure(figsize=(8, 5))
features, values = zip(*knn_imp)
plt.barh(
    features,
    values,
    color=plt.cm.viridis(np.linspace(0.3, 0.9, len(features))),
    edgecolor="black",
)
plt.xlabel("Снижение точности (Permutation Importance)")
plt.title("Важность признаков - KNN", fontsize=14, fontweight="bold")
plt.gca().invert_yaxis()
for i, v in enumerate(values):
    plt.text(v + 0.005, i, f"{v:.3f}", va="center", fontsize=9)
plt.tight_layout()
plt.show()


# 9. Decision Tree + GridSearchCV + Feature Importance + Визуализация дерева

dt = DecisionTreeClassifier(random_state=42)
dt_model = evaluate("Decision Tree", dt, X_train, X_test, y_train, y_test)

dt_params = {"max_depth": [3, 5, 7, None], "min_samples_split": [2, 5, 10]}
dt_grid = GridSearchCV(
    DecisionTreeClassifier(random_state=42), dt_params, cv=5, scoring="accuracy"
)
dt_grid.fit(X_train, y_train)
print(f"\nBest DT: {dt_grid.best_params_} | CV Score: {dt_grid.best_score_:.4f}")
best_dt = dt_grid.best_estimator_

# Gini Importance
dt_imp = sorted(
    zip(X.columns, best_dt.feature_importances_), key=lambda x: x[1], reverse=True
)

plt.figure(figsize=(8, 5))
features, values = zip(*dt_imp)
plt.barh(
    features,
    values,
    color=plt.cm.Greens(np.linspace(0.3, 0.9, len(features))),
    edgecolor="black",
)
plt.xlabel("Gini Importance")
plt.title("Важность признаков - Decision Tree", fontsize=14, fontweight="bold")
plt.gca().invert_yaxis()
for i, v in enumerate(values):
    plt.text(v + 0.005, i, f"{v:.3f}", va="center", fontsize=9)
plt.tight_layout()
plt.show()

# 10. Random Forest + Feature Importance

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model = evaluate("Random Forest", rf, X_train, X_test, y_train, y_test)

rf_imp = sorted(
    zip(X.columns, rf.feature_importances_), key=lambda x: x[1], reverse=True
)

plt.figure(figsize=(8, 5))
features, values = zip(*rf_imp)
plt.barh(
    features,
    values,
    color=plt.cm.Oranges(np.linspace(0.3, 0.9, len(features))),
    edgecolor="black",
)
plt.xlabel("Mean Decrease in Impurity")
plt.title("Важность признаков - Random Forest", fontsize=14, fontweight="bold")
plt.gca().invert_yaxis()
for i, v in enumerate(values):
    plt.text(v + 0.005, i, f"{v:.3f}", va="center", fontsize=9)
plt.tight_layout()
plt.show()


# 11. SVM + Permutation Importance

svm = SVC(random_state=42)
svm_model = evaluate("SVM", svm, X_train, X_test, y_train, y_test)

perm_svm = permutation_importance(svm, X_test, y_test, n_repeats=10, random_state=42)
svm_imp = sorted(
    zip(X.columns, perm_svm.importances_mean), key=lambda x: x[1], reverse=True
)

plt.figure(figsize=(8, 5))
features, values = zip(*svm_imp)
plt.barh(
    features,
    values,
    color=plt.cm.Purples(np.linspace(0.3, 0.9, len(features))),
    edgecolor="black",
)
plt.xlabel("Снижение точности (Permutation Importance)")
plt.title("Важность признаков - SVM", fontsize=14, fontweight="bold")
plt.gca().invert_yaxis()
for i, v in enumerate(values):
    plt.text(v + 0.005, i, f"{v:.3f}", va="center", fontsize=9)
plt.tight_layout()
plt.show()


# 12. Сводное сравнение моделей + визуализация

print("\n" + "=" * 60)
print("СРАВНЕНИЕ МОДЕЛЕЙ")
print("=" * 60)
print(f"{'Модель':<20} | {'Train Acc':<10} | {'Test Acc':<10} | {'Macro F1':<10}")
print("-" * 60)

results = []
for name, m in [
    ("KNN (opt)", best_knn),
    ("Decision Tree", best_dt),
    ("Random Forest", rf),
    ("SVM", svm),
]:
    test_pred = m.predict(X_test)
    train_acc = accuracy_score(y_train, m.predict(X_train))
    test_acc = accuracy_score(y_test, test_pred)
    macro_f1 = classification_report(
        y_test, test_pred, output_dict=True, zero_division=0
    )["macro avg"]["f1-score"]
    results.append(
        {
            "Model": name,
            "Train Acc": train_acc,
            "Test Acc": test_acc,
            "Macro F1": macro_f1,
        }
    )
    print(f"{name:<20} | {train_acc:<10.4f} | {test_acc:<10.4f} | {macro_f1:<10.4f}")

# Визуализация 1: Группированный бар-чарт
results_df = pd.DataFrame(results)
results_melted = results_df.melt(id_vars="Model", var_name="Metric", value_name="Score")

plt.figure(figsize=(10, 6))
sns.barplot(
    data=results_melted,
    x="Model",
    y="Score",
    hue="Metric",
    palette={"Train Acc": "#2ecc71", "Test Acc": "#3498db", "Macro F1": "#e74c3c"},
    edgecolor="black",
)
plt.ylabel("Score")
plt.title("Сравнение моделей по метрикам", fontsize=14, fontweight="bold")
plt.xticks(rotation=15, ha="right")
plt.legend(title="Метрика", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.axhline(y=0.8, color="gray", linestyle="--", linewidth=0.5, alpha=0.5)
plt.tight_layout()
plt.show()

# Визуализация 2: Только тестовая точность с выделением лидера
plt.figure(figsize=(8, 5))
best_idx = results_df["Test Acc"].idxmax()
colors = ["gold" if i == best_idx else "#3498db" for i in range(len(results_df))]
bars = plt.bar(
    results_df["Model"],
    results_df["Test Acc"],
    color=colors,
    edgecolor="black",
    alpha=0.9,
)
plt.axhline(
    y=results_df["Test Acc"].max(),
    color="red",
    linestyle="--",
    linewidth=1.5,
    label=f"Лучшая: {results_df['Test Acc'].max():.4f}",
)
plt.ylabel("Test Accuracy")
plt.title("Тестовая точность моделей", fontsize=14, fontweight="bold")
plt.xticks(rotation=15, ha="right")
plt.ylim(0.7, 1.0)
plt.legend()
for bar in bars:
    h = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        h + 0.005,
        f"{h:.3f}",
        ha="center",
        va="bottom",
        fontweight="bold",
    )
plt.tight_layout()
plt.show()

# Heatmap сводной таблицы
plt.figure(figsize=(8, 4))
heatmap_data = results_df.set_index("Model").T
sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".4f",
    cmap="YlOrRd",
    cbar_kws={"label": "Score"},
    linewidths=0.5,
)
plt.title("Сводная таблица результатов", fontsize=14, fontweight="bold")
plt.ylabel("Метрика")
plt.xlabel("Модель")
plt.xticks(rotation=15, ha="right")
plt.tight_layout()
plt.show()
