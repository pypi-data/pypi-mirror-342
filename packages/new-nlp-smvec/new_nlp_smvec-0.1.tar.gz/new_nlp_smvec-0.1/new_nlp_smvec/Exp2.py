#loaded a pre trained model

def perform_ner(text):
    # Load the English language model
    nlp = spacy.load('en_core_web_sm')
    
    # Process the input text
    doc = nlp(text)
    
    # Extract named entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    return entities
# Example text for NER
sample_text = "Mark Zuckerberg is one of the founders of Facebook, a company from the United States."
# Perform NER on the example text
ner_results = perform_ner(sample_text)

# Print the named entities and their labels
for entity, label in ner_results:
    print(f"Entity: {entity}, Label: {label}")
