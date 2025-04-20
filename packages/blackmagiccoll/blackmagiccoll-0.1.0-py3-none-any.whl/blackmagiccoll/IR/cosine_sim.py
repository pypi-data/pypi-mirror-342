from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample list of documents
documents = [
    "Machine learning is great",
    "Artificial intelligence is the future",
    "I love learning about AI and ML",
    "This is a random sentence"
]

# Step 1: Create the TF-IDF vectorizer and transform the documents
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)
print(tfidf_matrix.toarray())  # Print the TF-IDF matrix for debugging
print("Feature names:", vectorizer.get_feature_names_out())  # Print feature names for debugging

# Step 2: Function to find the most similar document to a query
def find_most_similar(query):
    query_vector = vectorizer.transform([query])  # Convert query to TF-IDF vector
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix)  # Compare with documents
    best_match_index = similarity_scores.argmax()  # Get index of best match
    return documents[best_match_index]  # Return the most similar document

# Example usage
query = "I want to learn AI"
result = find_most_similar(query)
print("Most similar document:", result)
