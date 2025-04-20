from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Corpus
corpus = [
    "India has the second-largest population in the world.",
    "It is surrounded by oceans from three sides which are Bay Of Bengal in the east, the Arabian Sea in the west and Indian Ocean in the south.",
    "Tiger is the national animal of India.",
    "Peacock is the national bird of India.",
    "Mango is the national fruit of India."
]

# Step 2: Query
query = "Where is Arabian sea?"

# Step 3: Vectorize
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus + [query])  # Add query to corpus
cos_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])  # Compare query with corpus

# Step 4: Get the most relevant sentence
most_similar_idx = cos_sim.argmax()
answer = corpus[most_similar_idx]

print("Question:", query)
print("Answer:", answer)
