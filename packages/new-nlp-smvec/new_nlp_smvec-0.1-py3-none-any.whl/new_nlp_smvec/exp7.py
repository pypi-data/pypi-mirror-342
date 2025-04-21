import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
import re


tokenizer = TreebankWordTokenizer()

# Sample dataset of tweets with sentiment labels (0 for negative, 1 for positive)
tweets = [
    ("I hate candidate A", 0),
    ("I love candidate B", 1),
    ("Candidate A is terrible", 0),
    ("I support candidate B", 1),
    ("Can't stand candidate A", 0),
    ("I'm voting for candidate B", 1)
]

# Convert the dataset into a DataFrame
df = pd.DataFrame(tweets, columns=['text', 'sentiment'])

# Preprocessing function
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize the text
    words = tokenizer.tokenize(text)

    # Remove stopwords
    words = [word for word in words if word not in stopwords.words('english')]
    # Return the preprocessed text as a single string
    return ' '.join(words)

# Apply preprocessing to the 'text' column
df['text'] = df['text'].apply(preprocess_text)

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['sentiment'], test_size=0.2, random_state=42)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(max_features=1000)
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train a Random Forest classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train_vectorized, y_train)

# Make predictions
y_pred = rf_classifier.predict(X_test_vectorized)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Print classification report
print(classification_report(y_test, y_pred))

# Create a DataFrame to store the sentiment scores for each tweet
sentiment_df = pd.DataFrame({'text': X_test, 'sentiment': y_test, 'predicted_sentiment': y_pred})
df['original_text'] = df['text']


# Add a column to indicate the candidate mentioned in each tweet
sentiment_df['candidate'] = sentiment_df['text'].apply(lambda x: 'A' if 'candidate a' in x else ('B' if 'candidate b' in x else None))

# Calculate the average sentiment score for each candidate
average_sentiment = sentiment_df.groupby('candidate')['predicted_sentiment'].mean()

# Determine the candidate with the highest average sentiment score
winning_candidate = average_sentiment.idxmax()

print(f"Candidate {winning_candidate} has the highest possibility of winning.")