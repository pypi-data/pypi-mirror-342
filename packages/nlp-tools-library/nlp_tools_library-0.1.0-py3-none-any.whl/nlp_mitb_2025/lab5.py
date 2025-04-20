class TextProcessor:
    def __init__(self):
        """Initialize the TextProcessor class."""
        import re
        from nltk.tokenize import RegexpTokenizer, word_tokenize
        self.re = re
        self.RegexpTokenizer = RegexpTokenizer
        self.word_tokenize = word_tokenize
    
    def count_digits(self, sentence):
        """Count the number of digits in a sentence."""
        tokenizer = self.RegexpTokenizer(r'\d')
        tokens = tokenizer.tokenize(sentence)
        return len(tokens)
    
    def extract_digits(self, sentence):
        """Extract all digit sequences from a sentence."""
        tokenizer = self.RegexpTokenizer(r'\d+')
        return tokenizer.tokenize(sentence)
    
    def greedy_tokenizer(self, sentence):
        """Perform greedy tokenization (dates & email addresses)."""
        patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z]+\.[a-zA-Z]{2,}'
        ]
        
        combined_pattern = '|'.join(patterns)
        tokenizer = self.RegexpTokenizer(combined_pattern)
        specific_tokens = tokenizer.tokenize(sentence)
        greedy_tokens = self.word_tokenize(self.re.sub(combined_pattern, " ", sentence))
        return specific_tokens + greedy_tokens
    
    def remove_digits(self, sentence):
        """Remove digits from a sentence."""
        new_sentence = self.re.sub(r'\d+', "", sentence)
        tokens = self.word_tokenize(new_sentence)
        return " ".join(tokens)
