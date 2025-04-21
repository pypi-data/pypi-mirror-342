#pip install sumy
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
nlp = spacy.load("en_core_web_sm")
def extract_text_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text
def generate_summary(text, num_sentences=2):
    # Preprocess text using spaCyu
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]

    # Join the sentences into a single string
    text = " ".join(sentences)

    # Use sumy to summarize the text
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)

    # Convert summary sentences back to string
    summary_text = " ".join([str(sentence) for sentence in summary])
    return summary_text
file_path = r"C:\Users\Shuhaib\Desktop\covid.txt"
document_text = extract_text_from_file(file_path)

# Generate summary
summary = generate_summary(document_text)

# Print the summary
print(summary)