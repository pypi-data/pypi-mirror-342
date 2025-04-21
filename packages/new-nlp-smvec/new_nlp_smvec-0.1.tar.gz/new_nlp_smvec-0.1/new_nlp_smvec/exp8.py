import spacy
from textblob import TextBlob
spacy.load('es_core_news_sm')
# Load Spanish language model 
nlp = spacy.load("es_core_news_sm") 
# Define text to analyze 
text ="La vida es como una bicicleta. Para mantener el equilibrio, debes seguir adelante."
# Tokenize text 
doc = nlp(text) 
# Print tokenized text with part-of-speech tags
for token in doc:
    print(token.text, token.pos_)

# Extract named entities and print them with their labels
for ent in doc.ents:
    print(ent.text, ent.label_)
    # Initialize sentiment score
sentiment_score = 0

# Iterate over each sentence in the document
for sentence in doc.sents:
    # Perform sentiment analysis on the sentence using TextBlob
    analysis = TextBlob(sentence.text)
    
    # Add the polarity score of the sentence to the sentiment score
    sentiment_score += analysis.sentiment.polarity

# Print sentiment score 
print("Sentiment score:", sentiment_score)