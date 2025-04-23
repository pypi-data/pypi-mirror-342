import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

iris_data = load_iris()
X = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
y = iris_data.target

print(f"Shape of original dataset: {X.shape}")

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA()
X_pca = pca.fit_transform(X_scaled)

explained_variance_ratio = pca.explained_variance_ratio_
cumulative_variance_ratio = np.cumsum(explained_variance_ratio)

plt.figure(figsize=(8, 5))
plt.plot(range(1, len(cumulative_variance_ratio) + 1), cumulative_variance_ratio, marker='o', linestyle='--')
plt.title('Explained Variance by Principal Components')
plt.xlabel('Number of Principal Components')
plt.ylabel('Cumulative Explained Variance')
plt.grid(True)
plt.show()

pca_optimal = PCA(n_components=2)
X_pca_optimal = pca_optimal.fit_transform(X_scaled)

pca_df = pd.DataFrame(data=X_pca_optimal, columns=['PC1', 'PC2'])
pca_df['Target'] = y


plt.figure(figsize=(8, 6))
colors = ['red', 'green', 'blue']
for target, color in zip(np.unique(y), colors):
    subset = pca_df[pca_df['Target'] == target]
    plt.scatter(subset['PC1'], subset['PC2'], color=color, label=f'Class {iris_data.target_names[target]}')

plt.title('Iris Dataset - PCA Visualization')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.grid(True)
plt.show()