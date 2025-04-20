import re
from collections import defaultdict
from typing import List, Dict, Union

class LazarTokenizer:
    def __init__(self):
        self.vocab: Dict[str, int] = {}
        self.inverse_vocab: Dict[int, str] = {}
        self.special_tokens: Dict[str, int] = {}
        self.unk_token = "[UNK]"
        self.pad_token = "[PAD]"
        self._regex_pattern = r"\w+|\S"
    
    def fit(self, texts: Union[List[str], str], vocab_size: int = 30000):
        """Build vocabulary from texts"""
        if isinstance(texts, str):
            texts = [texts]
        
        word_counts = defaultdict(int)
        for text in texts:
            words = re.findall(self._regex_pattern, text.lower())
            for word in words:
                word_counts[word] += 1
        
        # Sort by frequency and take top vocab_size
        sorted_words = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
        vocab_items = sorted_words[:vocab_size - len(self.special_tokens)]
        
        # Build vocabulary
        self.vocab = {**self.special_tokens}
        self.vocab.update({word: idx + len(self.special_tokens) 
                          for idx, (word, _) in enumerate(vocab_items)})
        
        self.inverse_vocab = {idx: word for word, idx in self.vocab.items()}
    
    def encode(self, text: str) -> List[int]:
        """Convert text to token IDs"""
        words = re.findall(self._regex_pattern, text.lower())
        return [self.vocab.get(word, self.vocab.get(self.unk_token, -1)) 
                for word in words]
    
    def decode(self, token_ids: List[int]) -> str:
        """Convert token IDs back to text"""
        return ' '.join(self.inverse_vocab.get(idx, self.unk_token) 
                       for idx in token_ids)
    
    def add_special_tokens(self, tokens: List[str]):
        """Add special tokens to vocabulary"""
        for token in tokens:
            if token not in self.special_tokens:
                self.special_tokens[token] = len(self.special_tokens)
        
        # Rebuild vocab if it already exists
        if self.vocab:
            self.fit(list(self.inverse_vocab.values()), 
                   vocab_size=len(self.vocab) + len(self.special_tokens))
