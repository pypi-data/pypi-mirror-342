import unittest
import os
from OctoLingo.history import TranslationHistory

class TestTranslationHistory(unittest.TestCase):
    def setUp(self):
        self.history_file = 'test_translation_history.json'
        self.history = TranslationHistory(self.history_file)

    def test_log_translation(self):
        # Test logging a translation
        self.history.log_translation("Hello", "Hola", "en", "es")
        history = self.history.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['source_text'], "Hello")

    def tearDown(self):
        # Clean up the test file
        if os.path.exists(self.history_file):
            os.remove(self.history_file)

if __name__ == '__main__':
    unittest.main()