import re

def clean_amharic_text(text):
    if not text:
        return ""
    text = re.sub(r'[^\u1200-\u137F\s]', '', text)  # Remove non-Amharic
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    return text.strip()

def tokenize_amharic(text):
    return text.split()
