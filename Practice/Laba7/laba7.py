import warnings

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import mode
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import load_digits, load_sample_image, make_blobs
from sklearn.metrics import accuracy_score, confusion_matrix

warnings.filterwarnings("ignore")

plt.rcParams["figure.figsize"] = (8, 6)
sns.set_theme(style="whitegrid")

# Генерация данных
X, _ = make_blobs(n_samples=600, centers=5, cluster_std=1.2, random_state=67)

# 1 K-Means для 5 кластеров
kmeans = KMeans(n_clusters=5, init="k-means++", n_init=10, random_state=67)
clusters_kmeans = kmeans.fit_predict(X)

# Визуализация
plt.scatter(
    X[:, 0], X[:, 1], c=clusters_kmeans, cmap="viridis", s=40, alpha=0.7, label="Данные"
)
plt.scatter(
    kmeans.cluster_centers_[:, 0],
    kmeans.cluster_centers_[:, 1],
    s=250,
    c="red",
    marker="X",
    edgecolors="black",
    label="Центроиды",
)
plt.title("Результат кластеризации K-Means (k=5)")
plt.xlabel("Признак 1")
plt.ylabel("Признак 2")
plt.legend()
plt.show()


# 2 Elbow Method
distortions = []
K_range = range(1, 11)

for k in K_range:
    kmeans_temp = KMeans(n_clusters=k, n_init=10, random_state=67)
    kmeans_temp.fit(X)
    distortions.append(kmeans_temp.inertia_)

plt.plot(K_range, distortions, "bo-", linewidth=2, markersize=8)
plt.xlabel("Количество кластеров (k)", fontsize=12)
plt.ylabel("Distortion (Inertia)", fontsize=12)
plt.title("Метод локтя для определения оптимального k", fontsize=14)
plt.xticks(K_range)
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

# 3 DBSCAN
# Подбор параметров (эмпирически для данного набора)
dbscan = DBSCAN(eps=1.8, min_samples=5)
clusters_dbscan = dbscan.fit_predict(X)

# Визуализация
unique_labels = set(clusters_dbscan)
colors = [plt.cm.Spectral(c) for c in np.linspace(0, 1, len(unique_labels))]
plt.scatter(X[:, 0], X[:, 1], c=clusters_dbscan, cmap="viridis", s=40, alpha=0.7)
plt.title("Результат кластеризации DBSCAN")
plt.xlabel("Признак 1")
plt.ylabel("Признак 2")
plt.show()

# 4 Предсказание чисел
digits = load_digits()
X_digits = digits.data

# 1. Кластеризация
kmeans_digits = KMeans(n_clusters=10, n_init=10, random_state=42)
clusters_digits = kmeans_digits.fit_predict(X_digits)

# 2. Сопоставление кластеров с истинными метками
labels = np.zeros_like(clusters_digits)
for i in range(10):
    mask = clusters_digits == i
    if np.any(mask):  # проверка, что в кластере есть точки
        # Используем np.bincount для быстрой и безопасной работы с целыми метками
        labels[mask] = np.bincount(digits.target[mask]).argmax()

# 3. Оценка точности
acc = accuracy_score(digits.target, labels)
print(f"Точность кластеризации (Accuracy): {acc:.4f}")

# 4. Матрица ошибок
mat = confusion_matrix(digits.target, labels)
plt.figure(figsize=(9, 7))
sns.heatmap(
    mat.T,
    square=True,
    annot=True,
    fmt="d",
    cbar=False,
    cmap="Blues",
    xticklabels=digits.target_names,
    yticklabels=digits.target_names,
)
plt.xlabel("Истинная метка", fontsize=12)
plt.ylabel("Предсказанная метка", fontsize=12)
plt.title("Матрица ошибок (Confusion Matrix)", fontsize=14)
plt.xticks(rotation=0)
plt.yticks(rotation=0)
plt.show()


# 5 Сжатие изображений
china = load_sample_image("china.jpg")

# 1. Подготовка данных
data = china / 255.0  # нормировка в [0, 1]
data = data.reshape(427 * 640, 3)

# 2. Кластеризация для уменьшения палитры (например, до 64 цветов)
n_colors = 64
print(f"Сжатие до {n_colors} цветов...")
kmeans_img = KMeans(n_clusters=n_colors, n_init=5, random_state=42)
labels_img = kmeans_img.fit_predict(data)
palette = kmeans_img.cluster_centers_

# 3. Восстановление изображения
compressed_data = palette[labels_img]
compressed_china = compressed_data.reshape(427, 640, 3)

# 4. Визуализация
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(china)
axes[0].set_title(f"Оригинал (256³ цветов)")
axes[0].axis("off")

axes[1].imshow(compressed_china)
axes[1].set_title(f"Сжатие ({n_colors} цветов)")
axes[1].axis("off")

plt.tight_layout()
plt.show()

# Оценка сжатия
original_size = china.nbytes
compressed_size = palette.nbytes + labels_img.nbytes
print(f"Исходный размер: {original_size:,} байт")
print(
    f"Размер сжатого: {compressed_size:,} байт ({(1 - compressed_size / original_size) * 100:.1f}% сжатия)"
)
