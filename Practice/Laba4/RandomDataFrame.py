import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Создаём DataFrame с 5 столбцами и 20 строками, заполненный случайными числами [0, 1]
# np.random.seed(42)  # для воспроизводимости
df = pd.DataFrame(np.random.rand(20, 5), columns=["A", "B", "C", "D", "E"])
print("Исходный DataFrame создан:")
print(df.head())

# 2. Считаем среднее значение для каждой строки → столбец "Avg"
df["Avg"] = df.mean(axis=1)
print("\nДобавлен столбец 'Avg':")
print(df[["A", "B", "Avg"]].head())

# 3. Нормализация столбца "Avg" по формуле: (x - xmin) / (xmax - xmin)
xmin = df["Avg"].min()
xmax = df["Avg"].max()
df["Norm"] = (df["Avg"] - xmin) / (xmax - xmin)
print("\nДобавлен нормализованный столбец 'Norm':")
print(df[["Avg", "Norm"]].head())

# 4. Столбец "Avg0.3": значения из "Avg", если > 0.3, иначе NaN
df["Avg0.3"] = df["Avg"].apply(lambda x: x if x > 0.3 else np.nan)
print("\nДобавлен столбец 'Avg0.3':")
print(df[["Avg", "Avg0.3"]].head(10))

# 5. Фильтрация: оставляем только строки, где "Avg0.3" не NaN → DataFrame2
df2 = df[df["Avg0.3"].notna()].copy()
print(f"\nDataFrame2 создан: {len(df2)} строк из {len(df)}")

# 6. Статистика для DataFrame2: min, max, mean для исходных столбцов (A-E)
stats = df2[["A", "B", "C", "D", "E"]].agg(["min", "max", "mean"])
print("\nСтатистика для DataFrame2:")
print(stats)


# 7. Столбец "Category" по значению Avg
def categorize(avg):
    if avg > 0.7:
        return "High"
    elif 0.4 <= avg <= 0.7:
        return "Medium"
    else:
        return "Low"


df["Category"] = df["Avg"].apply(categorize)
print("\nДобавлен столбец 'Category':")
print(df[["Avg", "Category"]].value_counts())

# 8. Сохранение в CSV-файлы
df.to_csv("ResultRandomDataFrame/dataframe_original.csv", index=False)
df2.to_csv("ResultRandomDataFrame/dataframe_filtered.csv", index=False)
print("\nДанные сохранены в 'dataframe_original.csv' и 'dataframe_filtered.csv'")

# 9. Гистограмма распределения одного из столбцов (например, 'A')
plt.figure(figsize=(8, 5))
plt.hist(df["A"], bins=10, edgecolor="black", color="skyblue")
plt.title('Распределение значений столбца "A"')
plt.xlabel("Значение")
plt.ylabel("Частота")
plt.grid(axis="y", alpha=0.75)
plt.tight_layout()
plt.savefig("ResultRandomDataFrame/histogram_A.png", dpi=300)
plt.show()
print("\nГистограмма сохранена как 'histogram_A.png'")
