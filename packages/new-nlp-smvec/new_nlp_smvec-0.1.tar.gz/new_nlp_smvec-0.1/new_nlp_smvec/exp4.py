from sklearn.feature_extraction.text import TfidfVectorizer  # Import the TF-IDF vectorizer

def extract_keywords(text, num_keywords=5):
    # Create a TF-IDF vectorizer with English stop words
    vectorizer = TfidfVectorizer(stop_words='english')

    # Fit and transform the text
    tfidf_matrix = vectorizer.fit_transform([text])

    # Get feature names and corresponding TF-IDF scores
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]

    # Get top 'num_keywords' keywords based on TF-IDF scores
    top_indices = tfidf_scores.argsort()[-num_keywords:][::-1]
    top_keywords = [feature_names[i] for i in top_indices]

    return top_keywords

# Example text for keyword extraction
example_text = """Natural language processing (NLP) is a field of artificial intelligence that focuses on the interaction between computers and humans using natural language. It involves the development of algorithms and models that enable computers to understand, interpret, and generate human-like language."""

# Extract keywords from the example text
keywords = extract_keywords(example_text, num_keywords=5)

# Print the extracted keywords
print("Keywords:", keywords)