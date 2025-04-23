import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

iris = load_iris()
data = pd.DataFrame(iris.data, columns=iris.feature_names)

scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

wcss = []  # Within-cluster sum of squares
cluster_range = range(1, 11)

for k in cluster_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(data_scaled)
    wcss.append(kmeans.inertia_)  # Inertia = Sum of squared distances to nearest centroid

plt.plot(cluster_range, wcss, marker='o')
plt.title('Elbow Method for Optimal Number of Clusters')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('WCSS (Within-Cluster Sum of Squares)')
plt.show()

optimal_clusters = 3  # Based on the elbow curve, for Iris, 3 is typically optimal
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42, n_init=10)
data['Cluster'] = kmeans.fit_predict(data_scaled)

plt.figure(figsize=(8, 6))
sns.scatterplot(data=data, x='sepal length (cm)', y='sepal width (cm)',
                hue='Cluster', palette='viridis', style='Cluster', s=100)
plt.title('K-Means Clustering of Iris Dataset')
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Sepal Width (cm)')
plt.legend(title='Cluster')
plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(data=data, x='petal length (cm)', y='petal width (cm)',
                hue='Cluster', palette='viridis', style='Cluster', s=100)
plt.title('K-Means Clustering of Iris Dataset (Petal Dimensions)')
plt.xlabel('Petal Length (cm)')
plt.ylabel('Petal Width (cm)')
plt.legend(title='Cluster')
plt.show()

cluster_characteristics = data.groupby('Cluster').mean()
print("Cluster Characteristics:")
print(cluster_characteristics)

