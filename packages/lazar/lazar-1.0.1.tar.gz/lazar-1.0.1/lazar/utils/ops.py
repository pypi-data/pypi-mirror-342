from typing import List, Callable, Any, TypeVar
import math

T = TypeVar('T')

def batch_process(data: List[T], 
                 batch_size: int, 
                 process_fn: Callable[[List[T]], Any]) -> List[Any]:
    """Process data in batches"""
    results = []
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        results.extend(process_fn(batch))
    return results

def parallel_map(func: Callable[[T], Any], 
                data: List[T], 
                chunksize: int = 1) -> List[Any]:
    """Simple parallel mapping (emulated for pure Python)"""
    # Note: Real implementation would use multiprocessing
    return [func(item) for item in data]
