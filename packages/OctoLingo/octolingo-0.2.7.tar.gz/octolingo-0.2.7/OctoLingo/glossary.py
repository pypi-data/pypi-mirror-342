class Glossary:
    def __init__(self):
        self.glossary = {}

    def add_term(self, term, translation):
        """Add a custom term and its translation to the glossary."""
        self.glossary[term] = translation

    def apply_glossary(self, text):
        """Apply the glossary to the text."""
        for term, translation in self.glossary.items():
            text = text.replace(term, translation)
        return text