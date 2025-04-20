class TextTokenizer:
    def __init__(self):
        """Initialize the TextTokenizer class."""
        import nltk
        from nltk.tokenize import word_tokenize, RegexpTokenizer
        self.word_tokenize = word_tokenize
        self.RegexpTokenizer = RegexpTokenizer
    
    def tokenize_text(self, text):
        """Split every word in the text."""
        return self.word_tokenize(text)
    
    def extract_dates(self, text):
        """Extract dates in DD-MM-YYYY format."""
        pattern = "\\d{2}-\\d{2}-\\d{4}"
        tokenizer = self.RegexpTokenizer(pattern)
        return tokenizer.tokenize(text)
    
    def extract_phone_numbers(self, text):
        """Extract phone numbers in various formats."""
        pattern = r"\d{3}-\d{3}-\d{4} | \d{10}"
        tokenizer = self.RegexpTokenizer(pattern)
        return tokenizer.tokenize(text)
