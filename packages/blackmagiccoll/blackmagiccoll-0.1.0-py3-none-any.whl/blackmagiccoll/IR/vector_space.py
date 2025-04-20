from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


documents = [
    "the sun is the star in the solar system",     # doc1
    "she wore beautiful dress at the party last night",  # doc2
    "the book on the table caught my attention immediately"  # doc3
]

query = "solar system"


vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents + [query])  # Add query as last item


query_vector = tfidf_matrix[-1]  # Last row is query
doc_vectors = tfidf_matrix[:-1]  # All rows except last are documents

similarities = cosine_similarity(query_vector, doc_vectors).flatten()


for i, score in enumerate(similarities):
    print(f"Similarity with doc{i+1}: {score:.4f}")

most_similar_doc_index = similarities.argmax()
print("\nMost relevant document:", f"doc{most_similar_doc_index+1}")
print("Content:", documents[most_similar_doc_index])
