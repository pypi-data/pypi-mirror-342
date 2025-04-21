from difflib import get_close_matches    #matches the words from the words list 

def build_autocorrect_model(words): 
    autocorrect_model = {}     
    for word in words: 
        autocorrect_model[word.lower()] = word 
    return autocorrect_model 

def autocorrect_input(input_text, autocorrect_model):
    corrected_text = ""
    words = input_text.split()

    for word in words:
        corrected_word = autocorrect_model.get(word.lower(), None)
        if corrected_word:
            corrected_text += corrected_word + " "
        else:
            closest_match = get_close_matches(word, autocorrect_model.keys(), n=1, cutoff=0.7) # Adjusted cutoff value
            if closest_match:
                corrected_text += autocorrect_model[closest_match[0]] + " "
            else:
                corrected_text += word + " "

    return corrected_text.strip()

def main(): 
    word_list = ['apple', 'banana', 'cat', 'dog', 'elephant', 'fish']    
    autocorrect_model = build_autocorrect_model(word_list) 
 
    input_text = "Bananega is a fruit and fishhes is an animal." 
    corrected_text = autocorrect_input(input_text, autocorrect_model)     
    print(corrected_text) 
 
if __name__ == '__main__': 
    main() 