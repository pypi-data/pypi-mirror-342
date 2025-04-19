# Импорт библиотек
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Загрузка и первичная обработка данных
file_path = "loco_11_corr.tsv"
df = pd.read_csv(file_path, sep='\t', encoding='utf-8')

# Преобразуем числовые столбцы с запятыми в точки (если такие есть)
for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].str.replace(',', '.', regex=False)
        try:
            df[col] = df[col].astype(float)
        except:
            continue

# Удалим нечисловые и категориальные столбцы, оставим только численные замеры
numeric_df = df.select_dtypes(include=[np.number])

# Масштабируем данные
scaler = StandardScaler()
X_scaled = scaler.fit_transform(numeric_df)

# Применим метод Isolation Forest для поиска аномалий
iso_forest = IsolationForest(contamination=0.05, random_state=42)
df['anomaly_score'] = iso_forest.fit_predict(X_scaled)
df['is_anomaly'] = df['anomaly_score'] == -1

# Визуализация распределения признаков и аномалий
plt.figure(figsize=(10, 6))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
plt.title('Корреляционная матрица признаков')
plt.show()

# Количество аномалий
print("Количество аномалий:", df['is_anomaly'].sum())

# Визуализация по двум главным признакам
plt.figure(figsize=(8, 6))
sns.scatterplot(x=numeric_df.iloc[:, 0], y=numeric_df.iloc[:, 1], hue=df['is_anomaly'])
plt.title('Аномалии на 2D-графике по первым двум признакам')
plt.show()

# Разделение данных на выборки (если аномалий много)
if df['is_anomaly'].sum() > 0:
    clean_data = df[~df['is_anomaly']].drop(columns=['anomaly_score', 'is_anomaly'])
    anomaly_data = df[df['is_anomaly']].drop(columns=['anomaly_score', 'is_anomaly'])

    # Пример: делим чистые данные на train/test
    train, test = train_test_split(clean_data, test_size=0.2, random_state=42)
    print(f"Размер обучающей выборки: {train.shape}, тестовой: {test.shape}")
else:
    print("Аномалии не обнаружены, можно использовать весь датасет для обучения.")
