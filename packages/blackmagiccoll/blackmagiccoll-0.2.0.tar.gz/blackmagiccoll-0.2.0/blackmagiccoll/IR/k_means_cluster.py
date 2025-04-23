import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt


documents = [
    "The cat sat on the mat",
    "Dogs are great pets",
    "Cats are better than dogs",
    "Python is a programming language",
    "I love programming in Python",
    "Data science is awesome",
    "Machine learning is the future",
    "Deep learning and machine learning are different",
    "The dog chased the cat",
    "I enjoy writing Python scripts"
]

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

k = 3  
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(X)

sil_score = silhouette_score(X, kmeans.labels_)
print(f"Silhouette Score: {sil_score}")

print("\nCluster Centers (Top Terms):")
order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names_out()

for i in range(k):
    print(f"Cluster {i}:")
    for ind in order_centroids[i, :10]:  # Print top 10 terms per cluster
        print(f' {terms[ind]}')

labels = kmeans.labels_

df = pd.DataFrame({'Document': documents, 'Cluster': labels})
print("\nDocument Clusters:")
print(df)

from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X.toarray())

plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=labels, cmap='viridis')
plt.title('K-means Clustering of Documents')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.show()
