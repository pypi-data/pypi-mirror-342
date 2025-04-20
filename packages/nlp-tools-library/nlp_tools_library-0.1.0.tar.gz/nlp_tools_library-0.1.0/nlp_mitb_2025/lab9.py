class NLPProcessor:
    def __init__(self, use_multilingual=False):
        """Initialize the NLPProcessor class with either English or multilingual models."""
        import spacy
        try:
            self.nlp = spacy.load("en_core_web_sm") if not use_multilingual else spacy.load("xx_ent_wiki_sm")
        except:
            raise ImportError("Required spaCy models not installed. Use 'python -m spacy download en_core_web_sm' or 'python -m spacy download xx_ent_wiki_sm'")
    
    def process_text(self, text, language="en"):
        """Process text using spaCy to extract POS tags, dependencies, noun phrases, and entities."""
        doc = self.nlp(text)
        
        pos_tags = [(token.text, token.pos_) for token in doc]
        dependencies = [(token.text, token.dep_, token.head.text) for token in doc]
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        return {
            'pos_tags': pos_tags,
            'dependencies': dependencies,
            'noun_phrases': noun_phrases,
            'entities': entities,
            'doc': doc  # Return the spaCy doc object for further processing
        }
