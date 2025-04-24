from stop_words import get_stop_words
import re
from rank_bm25 import BM25Okapi

class BM25Corpus:
    # Language should be german or english
    def __init__(self, texts:list[str], language:str):
        self.texts = texts
        self.language = language
        if self.language == 'de':
            self.stopwords = get_stop_words('de')
        elif self.language == 'en':
            self.stopwords = get_stop_words('en')
        else:
            raise ValueError("Unsupported language: choose 'de' for German or 'en' for English")
    
    def clean_token(self):
        cleaned_texts = []
        for text in self.texts:
            cleaned_tokens = []
            # Split sentence into words
            for token in text.lower().split():
                # Remove all punctuations (both leading, trailing, and inside words)
                token = re.sub(r'[^\w\s]', '', token)  # Remove punctuation
                # Filter out stop words and empty tokens
                if len(token) > 0 and token not in self.stopwords:
                    cleaned_tokens.append(token)
            cleaned_texts.append(cleaned_tokens)
        # Return list of cleaned tokens
        self.cleaned_texts = cleaned_texts
        # return cleaned_texts
    
    def create_corpus(self):
        return BM25Okapi(self.cleaned_texts)