import re
import unicodedata

def clean_text(text):
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()
