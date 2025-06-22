import re

def simple_amharic_tokenizer(text):
    """
    Tokenize Amharic by splitting on whitespace and punctuation.
    """
    tokens = re.findall(r'\S+', text)
    return tokens
