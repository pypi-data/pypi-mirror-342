import unittest
from OctoLingo.utils import split_text_into_chunks

class TestUtils(unittest.TestCase):
    def test_split_text_into_chunks(self):
        # Test splitting text into chunks
        text = "Hello. This is a test. " * 1000
        chunks = split_text_into_chunks(text)
        self.assertTrue(len(chunks) > 1)
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 4900)

if __name__ == '__main__':
    unittest.main()