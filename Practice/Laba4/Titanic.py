import matplotlib.pyplot as plt
import pandas as pd

# Загрузка и обработка пропущенных значений
titanic = pd.read_csv("DatasetsTitanic/titanic.csv")  # укажите правильный путь к файлу

print("Проверка пропущенных значений:")
print(titanic.isnull().sum())

# Заполняем пропуски в Age медианой
titanic["Age"].fillna(titanic["Age"].median(), inplace=True)

# Заполняем пропуски в Embarked модой (наиболее частое значение)
titanic["Embarked"].fillna(titanic["Embarked"].mode()[0], inplace=True)

print("\nПропущенные значения обработаны")

# Общая статистика и анализ
print("\nОбщая статистика (describe):")
print(titanic.describe())

# Количество выживших / погибших
survived_counts = titanic["Survived"].value_counts()
print(f"\nВыжившие: {survived_counts.get(1, 0)}, Погибшие: {survived_counts.get(0, 0)}")

# Средний возраст по классам кают
avg_age_by_class = titanic.groupby("Pclass")["Age"].mean()
print("\nСредний возраст по классам кают:")
print(avg_age_by_class)

# Самый пожилой и самый молодой пассажир
oldest = titanic.loc[titanic["Age"].idxmax()]
youngest = titanic.loc[titanic["Age"].idxmin()]
print(
    f"\nСамый пожилой: {oldest['Name']}, возраст: {oldest['Age']}, выжил: {'Да' if oldest['Survived'] == 1 else 'Нет'}"
)
print(
    f"Самый молодой: {youngest['Name']}, возраст: {youngest['Age']}, выжил: {'Да' if youngest['Survived'] == 1 else 'Нет'}"
)

# Мужчины и женщины среди выживших
gender_survived = titanic[titanic["Survived"] == 1]["Sex"].value_counts()
print("\nПол среди выживших:")
print(gender_survived)

# Новые столбцы: Family Size и AgeGroup
titanic["Family Size"] = titanic["SibSp"] + titanic["Parch"] + 1


def age_group(age):
    if age < 12:
        return "child"
    elif 12 <= age < 18:
        return "teenager"
    elif 18 <= age <= 60:
        return "adult"
    else:
        return "senior"


titanic["AgeGroup"] = titanic["Age"].apply(age_group)
print("\nДобавлены столбцы 'Family Size' и 'AgeGroup'")


# Столбец FareCategory
def fare_category(fare):
    if fare < 10:
        return "Low"
    elif 10 <= fare <= 50:
        return "Medium"
    else:
        return "High"


titanic["FareCategory"] = titanic["Fare"].apply(fare_category)
print("Добавлен столбец 'FareCategory'")

# Фильтрация данных
# Пассажиры, путешествовавшие в одиночку
solo_passengers = titanic[titanic["Family Size"] == 1]
print(f"\nПассажиры в одиночку: {len(solo_passengers)}")

# Первый класс + выжили
first_class_survivors = titanic[(titanic["Pclass"] == 1) & (titanic["Survived"] == 1)]
print(f"Выжившие пассажиры 1-го класса: {len(first_class_survivors)}")

# Билет > 100 и без семьи
rich_lonely = titanic[(titanic["Fare"] > 100) & (titanic["Family Size"] == 1)]
print(f"Пассажиры с билетом > $100 и без семьи: {len(rich_lonely)}")
print(rich_lonely[["Name", "Fare", "Family Size", "Survived"]].head())

print(titanic)
print(titanic[(titanic.Cabin == "C123") & (titanic.FareCategory == "High")])

# Визуализация
plt.figure(figsize=(15, 10))

# Гистограмма возрастов
plt.subplot(1, 3, 1)
plt.hist(titanic["Age"].dropna(), bins=30, edgecolor="black", color="lightgreen")
plt.title("Распределение возрастов")
plt.xlabel("Возраст")
plt.ylabel("Количество")

# Круговая диаграмма выживших
plt.subplot(1, 3, 2)
titanic["Survived"].map({0: "Погиб", 1: "Выжил"}).value_counts().plot.pie(
    autopct="%1.1f%%", startangle=90, colors=["lightcoral", "lightgreen"]
)
plt.title("Доля выживших и погибших")
plt.ylabel("")

# Boxplot цен на билеты по классам
# plt.subplot(1, 3, 3)
# titanic.boxplot(column="Fare", by="Pclass", patch_artist=True, showfliers=False)
# plt.title("Распределение цен по классам")
# plt.suptitle("")
# plt.xlabel("Класс каюты")
# plt.ylabel("Цена билета ($)")

plt.subplot(1, 3, 3)
fare_by_class = [titanic[titanic["Pclass"] == i]["Fare"].dropna() for i in [1, 2, 3]]
bp = plt.boxplot(
    fare_by_class, tick_labels=["1 класс", "2 класс", "3 класс"], patch_artist=True
)
plt.title("Распределение цен по классам")
plt.xlabel("Класс каюты")
plt.ylabel("Цена билета ($)")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("ResultTitanic/titanic_visualizations.png", dpi=300)
plt.show()
print("\nВизуализации сохранены как 'titanic_visualizations.png'")

# Сохранение обработанных данных
titanic.to_csv("ResultTitanic/titanic_cleaned.csv", index=False)
titanic[titanic["Survived"] == 1].to_csv(
    "ResultTitanic/titanic_survivors.csv", index=False
)
print("\nОбработанные данные сохранены:")
print("   • titanic_cleaned.csv — полный обработанный датасет")
print("   • titanic_survivors.csv — только выжившие пассажиры")
