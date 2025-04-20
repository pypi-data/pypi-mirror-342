class TextNormalizer:
    def __init__(self):
        """Initialize the TextNormalizer class."""
        from nltk.stem import WordNetLemmatizer, PorterStemmer
        from nltk.tokenize import word_tokenize
        import re
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()
        self.tokenize = word_tokenize
        self.re = re
    
    def stem_tokens(self, tokens):
        """Apply stemming to a list of tokens."""
        return [self.stemmer.stem(t) for t in tokens]
    
    def lemmatize_tokens(self, tokens):
        """Apply lemmatization to a list of tokens."""
        return [self.lemmatizer.lemmatize(t) for t in tokens]
    
    def clean_tokenize(self, text):
        """Clean and tokenize text by removing URLs, user mentions, hashtags, and punctuation."""
        text = self.re.sub(r"http\S+|@\w+|#\w+|[^\w\s]", '', text.lower())
        return self.tokenize(text)
    
    def normalize_text(self, text):
        """Normalize text by replacing dates, numbers, and other entities."""
        return self.re.sub(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\$\d+[\d,\.]*|\b\d+\b', 'ENTITY', text)
