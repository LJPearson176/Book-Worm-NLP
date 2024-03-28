import re
from num2words import num2words
import emoji
import contractions

def expand_contractions(text):
    """Expand common contractions in the given text using the contractions library."""
    return contractions.fix(text)

def convert_emojis_to_text(text):
    """Convert all emojis in the text to their description, with a space added before and after the description to ensure it's recognized as a separate word."""
    return emoji.demojize(text, delimiters=(" ", " "))

def replace_underscores(text):
    """Replace all underscores with spaces in the given text."""
    return text.replace('_', ' ')

def convert_numbers_to_words(text):
    """Convert all numeric digits to words in the given text."""
    return ' '.join([num2words(word) if word.isdigit() else word for word in text.split()])

def clean_text(text):
    """Lowercase and remove specified punctuation and symbols from text."""
    text = text.lower()
     # Remove reference notations
    text = re.sub(r'\[\d+\]', '', text)
    # Insert space between letters and directly following numbers
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    # Updated regex pattern to remove specified symbols including underscores
    text = re.sub(r'[,\;\:\[\]\{\}\|\&%\$#~`\+\-]', '', text)
    # Further remove any characters not alphanumeric or spaces
    text = re.sub(r'[^a-z0-9\s.?!]', '', text)
    return text


    
