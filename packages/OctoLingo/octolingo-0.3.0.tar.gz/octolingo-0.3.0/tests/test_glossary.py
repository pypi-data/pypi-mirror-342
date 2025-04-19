import unittest
from OctoLingo.glossary import Glossary

class TestGlossary(unittest.TestCase):
    def setUp(self):
        self.glossary = Glossary()

    def test_add_term(self):
        # Test adding a term to the glossary
        self.glossary.add_term("Hello", "Hola")
        self.assertEqual(self.glossary.glossary["Hello"], "Hola")

    def test_apply_glossary(self):
        # Test applying the glossary to text
        self.glossary.add_term("Hello", "Hola")
        result = self.glossary.apply_glossary("Hello, world!")
        self.assertEqual(result, "Hola, world!")

if __name__ == '__main__':
    unittest.main()