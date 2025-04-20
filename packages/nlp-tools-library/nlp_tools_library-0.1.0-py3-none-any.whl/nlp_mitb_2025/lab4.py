class NGramAnalyzer:
    def __init__(self):
        """Initialize the NGramAnalyzer class."""
        import nltk
        from nltk.util import ngrams
        from collections import Counter
        self.nltk = nltk
        self.ngrams = ngrams
        self.Counter = Counter
    
    def count_ngrams_freq(self, txt, reversed_txt, n):
        """Generate frequencies, reverse and calculate probabilities for n-gram."""
        tokens = self.nltk.word_tokenize(txt.lower())
        reversed_tokens = self.nltk.word_tokenize(reversed_txt.lower())

        n_grams = self.ngrams(tokens, n)
        n_grams_reversed = self.ngrams(reversed_tokens, n)

        n_grams = list(n_grams)
        n_grams_reversed = list(n_grams_reversed)

        freq = self.Counter(n_grams)
        freq_reversed = self.Counter(n_grams_reversed)

        total = len(n_grams)
        prob = {gram: round(count/total, 2) for gram, count in freq.items()}
        
        return freq, freq_reversed, prob
    
    def reverse_text(self, text):
        """Reverse the order of words in a text."""
        words = text.split()
        words = words[::-1]
        return ' '.join(words)
