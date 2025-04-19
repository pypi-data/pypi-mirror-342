import unittest
import os
from OctoLingo.file_handler import FileHandler

class TestFileHandler(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_file.txt'
        with open(self.test_file, 'w') as f:
            f.write("Hello, world!")

    def test_read_file(self):
        # Test reading a file
        content = FileHandler.read_file(self.test_file)
        self.assertEqual(content, "Hello, world!")

    def test_write_file(self):
        # Test writing to a file
        FileHandler.write_file('test_output.txt', "Hola, mundo!")
        with open('test_output.txt', 'r') as f:
            content = f.read()
        self.assertEqual(content, "Hola, mundo!")

    def tearDown(self):
        # Clean up test files
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists('test_output.txt'):
            os.remove('test_output.txt')

if __name__ == '__main__':
    unittest.main()