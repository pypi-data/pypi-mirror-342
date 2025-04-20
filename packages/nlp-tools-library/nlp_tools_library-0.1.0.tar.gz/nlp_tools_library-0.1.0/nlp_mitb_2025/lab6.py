class TextCleaner:
    def __init__(self):
        """Initialize the TextCleaner class."""
        import re
        import nltk
        from nltk.corpus import stopwords
        self.re = re
        self.stopwords = set(stopwords.words('english'))
    
    def clean_text(self, text):
        """Remove hashtags, special characters, and stopwords."""
        text = self.re.sub(r'#\w+|[^a-zA-Z\s]', "", text.lower())
        return " ".join(word for word in text.split() if word not in self.stopwords)
    
    def remove_emojis(self, text):
        """Remove emojis from text."""
        words = self.re.findall(r'[\w\s\.,!?;:\'"()-]+', text)
        return ''.join(words)
    
    def normalize(self, text):
        """Normalize text by converting to lowercase and standardizing whitespace."""
        return " ".join(text.lower().strip().split())
    
    def extract_dates(self, text):
        """Extract dates from text."""
        pattern = r'\b\d{1,2}([/-])\d{1,2}\1\d{4}\b'
        return [match.group(0) for match in self.re.finditer(pattern, text)]
    
    def standardize_phone_numbers(self, text):
        """Standardize phone numbers in the text."""
        pattern = self.re.compile(
            r'(\+?\d{1,2})?[\s\.-]?(\(?\d{3}\)?)?[\s\.-]?(\d{3})[\s\.-]?(\d{4})'
        )

        def format_match(match):
            country = match[0] if match[0] else "+1"
            area = match[1].strip("()") if match[1] else "000"
            return f"{country}-{area}-{match[2]}-{match[3]}"

        return [format_match(m) for m in pattern.findall(text)]
