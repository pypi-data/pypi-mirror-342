from .array import LazarArray
import math

def exp(arr: LazarArray) -> LazarArray:
    """Element-wise exponential."""
    return LazarArray([math.exp(x) for x in arr], arr.dtype)

def log(arr: LazarArray) -> LazarArray:
    """Element-wise natural logarithm."""
    return LazarArray([math.log(x) for x in arr], arr.dtype)

def sin(arr: LazarArray) -> LazarArray:
    """Element-wise sine."""
    return LazarArray([math.sin(x) for x in arr], arr.dtype)

def cos(arr: LazarArray) -> LazarArray:
    """Element-wise cosine."""
    return LazarArray([math.cos(x) for x in arr], arr.dtype)

def sqrt(arr: LazarArray) -> LazarArray:
    """Element-wise square root."""
    return LazarArray([math.sqrt(x) for x in arr], arr.dtype)
