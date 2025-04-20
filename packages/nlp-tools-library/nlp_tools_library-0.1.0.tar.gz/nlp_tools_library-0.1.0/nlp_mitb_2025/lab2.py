class SpecialCharHandler:
    def __init__(self):
        """Initialize the SpecialCharHandler class."""
        import re
        self.re = re
    
    def remove_special(self, txt):
        """Remove special characters from beginning and end of string."""
        return self.re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', "", txt)
    
    def count_special(self, txt):
        """Count special characters in a string."""
        special = self.re.findall("[^a-zA-Z0-9]+", txt)
        return sum(len(chars) for chars in special)
    
    def replace_special(self, txt, char="#"):
        """Replace special characters with a specified character."""
        return self.re.sub(r"[^a-zA-Z0-9]", char, txt)
