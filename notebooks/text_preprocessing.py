from nltk.corpus import stopwords
from nltk import word_tokenize
import re
    
# Clean the tokens (remove stopwords, punctuation, etc.)
def clean_text(input_text):
    
    # Lower text
    input_text = input_text.lower()
    
    # Tokenize text
    tokens = word_tokenize(input_text)

    # Remove stopwords
    stop_words = stopwords.words('english')
    tokens = [re.sub(r'[^\w\s]|_','', token) for token in tokens if token not in stop_words]

    # Remove short words
    tokens = [token.strip() for token in tokens if len(token) > 2]
    
    return tokens

# Clean an individual string
def individual_listing_text(line, vocab):
    
    # Clean the line of text
    clean_line = clean_text(line)
    
    # Keep only words in vocab
    clean_line = [token for token in clean_line if token in vocab]
    
    # Put it back together
    return ' '.join(clean_line)

# Clean an entire dataframe
def process_all_lines(dataframe, vocab):
    lines = []
    for listing in dataframe['name']:
        cleaned_text = individual_listing_text(listing, vocab)
        lines.append(cleaned_text)
    
    # Output is a list where each item is one listing where the text is cleaned
    return lines