# pip install pyspellchecker
from spellchecker import SpellChecker

def correct_spelling(text):
    spell = SpellChecker()

    # Tokenize the text into words
    words = text.split()

    corrected_text = []
    for word in words:
        # Get the corrected version of each word
        corrected_word = spell.correction(word)
        corrected_text.append(corrected_word)

    # Join the corrected words back into a sentence
    corrected_sentence = ' '.join(corrected_text)

    return corrected_sentence

# Example text with intentional spelling errors
sample_text = "Thiss is an examplee sentence with somme spellling mistakkes."

# Correct the spelling in the example text
corrected_text = correct_spelling(sample_text)

# Print the corrected text
print("Original text:", sample_text)
print("Corrected text:", corrected_text)
