import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
# Download NLTK data (if not already downloaded)
nltk.download('vader_lexicon')
def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)['compound']

    if sentiment_score >= 0.05:
        return "Positive"
    elif sentiment_score <= -0.05:
        return "Negative"
    else:
        return "Neutral" 
    # Example text for sentiment analysis
sample_text = "I enjoyed the movie. It was a great experience."
sample_text1 = "How are you"
# Analyze sentiment on the example text
sentiment_result = analyze_sentiment(sample_text)

# Print the sentiment result
print(f"Sentiment: {sentiment_result}")
# Analyze sentiment on the example text
sentiment_result1 = analyze_sentiment(sample_text1)

# Print the sentiment result
print(f"Sentiment: {sentiment_result1}")