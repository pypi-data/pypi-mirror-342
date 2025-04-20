import time
from functools import wraps
from typing import Callable, Any

def benchmark(func: Callable) -> Callable:
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} executed in {(end-start)*1000:.2f} ms")
        return result
    return wrapper

def compare_with_numpy(lazar_func: Callable, numpy_func: Callable, *args):
    """Compare performance between Lazar and Numpy implementation"""
    try:
        import numpy as np
        
        # Prepare numpy args
        np_args = []
        for arg in args:
            if isinstance(arg, LazarArray):
                np_args.append(np.array(arg._data).reshape(arg.shape))
            else:
                np_args.append(arg)
        
        # Benchmark numpy
        np_start = time.perf_counter()
        np_result = numpy_func(*np_args)
        np_time = time.perf_counter() - np_start
        
        # Benchmark lazar
        lz_start = time.perf_counter()
        lz_result = lazar_func(*args)
        lz_time = time.perf_counter() - lz_start
        
        print(f"\nPerformance Comparison ({lazar_func.__name__}):")
        print(f"Numpy: {np_time*1000:.2f} ms")
        print(f"Lazar: {lz_time*1000:.2f} ms")
        print(f"Ratio: {np_time/max(lz_time, 1e-9):.2f}x")
        
        return lz_result
    except ImportError:
        print("Numpy not available, skipping comparison")
        return lazar_func(*args)
