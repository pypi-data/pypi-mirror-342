class StringSplitter:
    def __init__(self):
        """Initialize the StringSplitter class."""
        import re
        import random
        self.re = re
        self.random = random
    
    def split_pairs(self, text):
        """Split the word in possible pairs, prefix and suffix, at all indexes."""
        output = []
        for i in range(1, len(text)):
            output.append((text[:i], text[i:]))
        return output
    
    def get_prefixes(self, text):
        """Get all prefixes of a string."""
        prefix = []
        for i in range(1, len(text)):
            prefix.append(text[:i])
        return prefix
    
    def get_suffixes(self, text):
        """Get all suffixes of a string."""
        suffix = []
        for i in range(1, len(text)):
            suffix.append(text[i:])
        return suffix
    
    def random_split(self, text):
        """Split a string at a random index."""
        n = self.random.randint(0, len(text))
        return text[:n], text[n:]
