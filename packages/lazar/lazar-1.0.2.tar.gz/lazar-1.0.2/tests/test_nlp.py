import unittest
from lazar.nl.tokenizer import LazarTokenizer

class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = LazarTokenizer()
        self.texts = ["Hello world!", "This is a test."]
    
    def test_tokenizer_fit(self):
        self.tokenizer.fit(self.texts)
        self.assertGreater(len(self.tokenizer.vocab), 0)
    
    def test_encode_decode(self):
        self.tokenizer.fit(self.texts)
        encoded = self.tokenizer.encode("Hello test")
        decoded = self.tokenizer.decode(encoded)
        self.assertIn("test", decoded.lower())

if __name__ == '__main__':
    unittest.main()
