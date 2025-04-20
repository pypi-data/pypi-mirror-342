class TextStandardizer:
    def __init__(self):
        """Initialize the TextStandardizer class."""
        import re
        self.re = re
        self.slang_dict = {
            "brb": "be right back",
            "lol": "laughing out loud",
            "omg": "oh my god",
            "ttyl": "talk to you later",
        }
        self.emoji_dict = {
            "😂": "laughing",
            "😊": "smiling",
            "😢": "crying",
            "🔥": "fire",
        }
    
    def standardize_text(self, text):
        """Standardize text by converting emojis, handling slang, and fixing punctuation."""
        text = text.lower()
        for emoji, replacement in self.emoji_dict.items():
            text = text.replace(emoji, f" {replacement} ")
        words = text.split()
        words = [self.slang_dict.get(word, word) for word in words]
        text = ' '.join(words)
        text = self.re.sub(r'([!?.,])\1+', r'\1', text)
        text = self.re.sub(r'\s+([!?.,])', r'\1', text)
        text = self.re.sub(r'\s+', ' ', text).strip()
        return text
    
    def update_emoji_dict(self, emoji_dict):
        """Update the emoji dictionary with new mappings."""
        self.emoji_dict.update(emoji_dict)
    
    def update_slang_dict(self, slang_dict):
        """Update the slang dictionary with new mappings."""
        self.slang_dict.update(slang_dict)
