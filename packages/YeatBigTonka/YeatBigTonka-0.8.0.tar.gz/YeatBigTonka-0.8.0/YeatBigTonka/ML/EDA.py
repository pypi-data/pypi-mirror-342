# Импорт библиотек
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
df = pd.read_csv("loco_11_corr.tsv", sep='\t', encoding='utf-8')

# Преобразование числовых столбцов с запятыми в точки
for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].str.replace(',', '.', regex=False)
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            continue

# Выводим информацию о датасете
print("=== Информация о данных ===")
df.info()
print("\n=== Описание числовых признаков ===")
print(df.describe())

# Выбираем только числовые признаки
numeric_cols = df.select_dtypes(include=[np.number]).columns

# График 1: Распределение одного из ключевых признаков
plt.figure(figsize=(8, 4))
sns.histplot(df[numeric_cols[0]], kde=True, bins=30)
plt.title(f"Распределение признака: {numeric_cols[0]}")
plt.grid(True)
plt.show()

# График 2: Boxplot по всем числовым признакам
plt.figure(figsize=(14, 6))
sns.boxplot(data=df[numeric_cols], orient='h')
plt.title("Boxplot по числовым признакам")
plt.grid(True)
plt.show()

# График 3: Корреляционная матрица
plt.figure(figsize=(12, 10))
sns.heatmap(df[numeric_cols].corr(), annot=True, fmt=".2f", cmap='coolwarm')
plt.title("Корреляционная матрица числовых признаков")
plt.show()
