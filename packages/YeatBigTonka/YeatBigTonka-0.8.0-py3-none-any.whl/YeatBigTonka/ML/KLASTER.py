# Импорт библиотек
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from pandas.plotting import parallel_coordinates
from mpl_toolkits.mplot3d import Axes3D

# Загрузка данных
df = pd.read_excel("Информация о пассажирах.xlsx")

# Преобразование пола в числовой формат
le = LabelEncoder()
df["Пол_код"] = le.fit_transform(df["Пол"])

# Выбор признаков для кластеризации
features = ["ID", "Пол_код", "Возраст", "Годовой доход (k$)", "Оценка по внутренним рейтингам"]
X = df[features]

# Масштабирование признаков
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Elbow method для выбора числа кластеров
inertia = []
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(k_range, inertia, marker='o')
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Inertia')
plt.grid(True)
plt.show()

# KMeans кластеризация (например, 4 кластера)
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans_labels = kmeans.fit_predict(X_scaled)
df["KMeans_cluster"] = kmeans_labels

# DBSCAN кластеризация
dbscan = DBSCAN(eps=1.2, min_samples=3)
dbscan_labels = dbscan.fit_predict(X_scaled)
df["DBSCAN_cluster"] = dbscan_labels

# Параллельные координаты
# KMeans
df_kmeans_plot = df[features + ["KMeans_cluster"]].copy()
df_kmeans_plot["KMeans_cluster"] = df_kmeans_plot["KMeans_cluster"].astype(str)
plt.figure(figsize=(12, 5))
parallel_coordinates(df_kmeans_plot, "KMeans_cluster", colormap='tab10')
plt.title("Параллельные координаты — KMeans")
plt.grid(True)
plt.show()

# DBSCAN
df_dbscan_plot = df[features + ["DBSCAN_cluster"]].copy()
df_dbscan_plot["DBSCAN_cluster"] = df_dbscan_plot["DBSCAN_cluster"].astype(str)
plt.figure(figsize=(12, 5))
parallel_coordinates(df_dbscan_plot, "DBSCAN_cluster", colormap='tab10')
plt.title("Параллельные координаты — DBSCAN")
plt.grid(True)
plt.show()

# 2D кластеризация (Возраст и Доход)
X_2d = X_scaled[:, [2, 3]]
fig, axs = plt.subplots(1, 2, figsize=(12, 5))
axs[0].scatter(X_2d[:, 0], X_2d[:, 1], c=kmeans_labels, cmap='tab10')
axs[0].set_title("KMeans (2D)")
axs[0].set_xlabel("Возраст")
axs[0].set_ylabel("Доход")
axs[1].scatter(X_2d[:, 0], X_2d[:, 1], c=dbscan_labels, cmap='tab10')
axs[1].set_title("DBSCAN (2D)")
axs[1].set_xlabel("Возраст")
axs[1].set_ylabel("Доход")
plt.tight_layout()
plt.show()

# 3D кластеризация (Пол, Возраст, Доход)
X_3d = X_scaled[:, [1, 2, 3]]
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_3d[:, 0], X_3d[:, 1], X_3d[:, 2], c=kmeans_labels, cmap='tab10')
ax.set_title("KMeans (3D)")
ax.set_xlabel("Пол")
ax.set_ylabel("Возраст")
ax.set_zlabel("Доход")
plt.show()

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_3d[:, 0], X_3d[:, 1], X_3d[:, 2], c=dbscan_labels, cmap='tab10')
ax.set_title("DBSCAN (3D)")
ax.set_xlabel("Пол")
ax.set_ylabel("Возраст")
ax.set_zlabel("Доход")
plt.show()