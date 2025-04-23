from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


documents = [
    "Machine learning is great",
    "Artificial intelligence is the future",
    "I love learning about AI and ML",
    "This is a random sentence"
]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)
print(tfidf_matrix.toarray())  
print("Feature names:", vectorizer.get_feature_names_out())  

def find_most_similar(query):
    query_vector = vectorizer.transform([query])  
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix) 
    best_match_index = similarity_scores.argmax()  
    return documents[best_match_index]  

query = "I want to learn AI"
result = find_most_similar(query)
print("Most similar document:", result)
