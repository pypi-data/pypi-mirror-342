import math
from typing import List, Tuple
from ..core.array import LazarArray

class LazarLanguageModel:
    def __init__(self, vocab_size: int, embedding_dim: int = 128):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        
        # Initialize weights
        self.embeddings = self._init_weights((vocab_size, embedding_dim))
        self.position_emb = self._init_weights((1000, embedding_dim))  # Max 1000 tokens
        self.output_weights = self._init_weights((embedding_dim, vocab_size))
    
    def _init_weights(self, shape: Tuple[int, int]) -> LazarArray:
        """Xavier initialization"""
        limit = math.sqrt(6 / sum(shape))
        data = [limit * (2 * math.random() - 1) for _ in range(math.prod(shape))]
        return LazarArray(data).reshape(shape)
    
    def embed(self, token_ids: List[int]) -> LazarArray:
        """Convert token IDs to embeddings"""
        embeddings = [self.embeddings[idx] for idx in token_ids]
        
        # Add positional embeddings
        positions = list(range(len(token_ids)))
        pos_embeddings = [self.position_emb[pos] for pos in positions]
        
        # Combine
        combined = [e + p for e, p in zip(embeddings, pos_embeddings)]
        return LazarArray(combined).reshape((len(token_ids), self.embedding_dim))
    
    def predict_next_token(self, embeddings: LazarArray) -> LazarArray:
        """Predict next token probabilities"""
        # Simple feedforward
        logits = embeddings.dot(self.output_weights)
        return self._softmax(logits)
    
    def _softmax(self, x: LazarArray) -> LazarArray:
        """Stable softmax implementation"""
        exp_values = [math.exp(val - max(x)) for val in x]
        sum_exp = sum(exp_values)
        return LazarArray([ev / sum_exp for ev in exp_values])
