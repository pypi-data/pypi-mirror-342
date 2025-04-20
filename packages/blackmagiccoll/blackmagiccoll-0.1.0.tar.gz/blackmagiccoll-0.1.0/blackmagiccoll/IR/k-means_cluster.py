import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# Sample documents (replace this with your dataset)
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

# Step 1: Preprocess documents and convert to TF-IDF vectors
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

# Step 2: Apply K-means clustering
k = 3  # You can choose the number of clusters based on your data or use methods like the elbow method to determine this
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(X)

# Step 3: Evaluate clustering with silhouette score
sil_score = silhouette_score(X, kmeans.labels_)
print(f"Silhouette Score: {sil_score}")

# Step 4: Print cluster centers and assign documents to clusters
print("\nCluster Centers (Top Terms):")
order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names_out()

for i in range(k):
    print(f"Cluster {i}:")
    for ind in order_centroids[i, :10]:  # Print top 10 terms per cluster
        print(f' {terms[ind]}')

# Step 5: Assign each document to a cluster
labels = kmeans.labels_

# Print the documents and their corresponding clusters
df = pd.DataFrame({'Document': documents, 'Cluster': labels})
print("\nDocument Clusters:")
print(df)

# Optional: Plot the clusters (if dimensionality reduction is necessary, like using PCA)
from sklearn.decomposition import PCA

# Reduce dimensionality to 2D for visualization
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X.toarray())

plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=labels, cmap='viridis')
plt.title('K-means Clustering of Documents')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.show()
