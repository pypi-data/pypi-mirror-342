import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Sample corpus
corpus = [
    "Hello! How can I assist you about the admission?",
    "What courses are available?",
    "We offer B.Tech, B.Sc, and BCA programs.",
    "What is the last date to apply?",
    "The last date for application is 30th April.",
    "What is the admission process?",
    "You need to fill out the online form and attend the counseling.",
    "Thank you!",
    "You're welcome.",
    "How much is the fee?",
    "The fee structure varies per course. Please check our website."
]

# Preprocess text
def preprocess(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    lemmatized = [lemmatizer.lemmatize(word) for word in tokens if word not in string.punctuation]
    return ' '.join(lemmatized)

# Preprocess the corpus
processed_corpus = [preprocess(sentence) for sentence in corpus]

# Initialize the vectorizer and fit on processed corpus
vectorizer = TfidfVectorizer()
tfidf_corpus = vectorizer.fit_transform(processed_corpus)

# Chat function
def chatbot_response(user_input):
    user_input_processed = preprocess(user_input)
    tfidf_input = vectorizer.transform([user_input_processed])
    similarity = cosine_similarity(tfidf_input, tfidf_corpus)
    idx = similarity.argmax()
    score = similarity[0][idx]

    if score > 0.3:
        return corpus[idx]
    else:
        return "I'm sorry, I don't have an answer for that. Please contact the admission office."

# Main chat loop
print("AdmissionBot: Hello! Ask me anything about admissions. Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'bye', 'quit']:
        print("AdmissionBot: Goodbye! All the best.")
        break
    response = chatbot_response(user_input)
    print("AdmissionBot:", response)
