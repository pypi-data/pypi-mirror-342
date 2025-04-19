import unittest
from OctoLingo.translator import OctoLingo
from OctoLingo.exceptions import TranslationError

class TestUniversalTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = OctoLingo()

    def test_validate_language(self):
        # Test supported language
        self.assertTrue(self.translator.validate_language('es'))
        # Test unsupported language
        with self.assertRaises(TranslationError):
            self.translator.validate_language('xx')

    def test_detect_language(self):
        # Test language detection
        lang, confidence = self.translator.detect_language("Hola, cómo estás?")
        self.assertEqual(lang, 'es')
        self.assertIsInstance(confidence, float)

    def test_translate(self):
        # Test translation
        translated_text, confidence = self.translator.translate("Hello, world!", 'es')
        self.assertIsInstance(translated_text, str)
        self.assertIsInstance(confidence, float)

    def test_translate_batch(self):
        # Test batch translation
        texts = ["Hello", "Goodbye"]
        results = self.translator.translate_batch(texts, 'es')
        self.assertEqual(len(results), 2)
        for translated_text, confidence in results:
            self.assertIsInstance(translated_text, str)
            self.assertIsInstance(confidence, float)

if __name__ == '__main__':
    unittest.main()