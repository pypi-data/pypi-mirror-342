import array
import math
import operator
from functools import partial
from typing import Union, Tuple, List

class LazarArray:
    __slots__ = ['_data', '_shape', '_dtype']
    
    DTYPE_MAP = {
        'float32': 'f',
        'int32': 'i',
        'uint8': 'B',
        'float64': 'd',
        'int64': 'q'
    }
    
    def __init__(self, data, dtype: str = 'float64'):
        self._dtype = dtype
        array_type = self.DTYPE_MAP.get(dtype)
        if array_type is None:
            raise ValueError(f"Unsupported dtype: {dtype}")
        
        if isinstance(data, (list, tuple)):
            self._data = array.array(array_type, data)
            self._shape = (len(data),)
        elif isinstance(data, array.array):
            if data.typecode != array_type:
                raise ValueError("Array typecode mismatch with dtype")
            self._data = data
            self._shape = (len(data),)
        else:
            raise TypeError("Input must be list, tuple or array.array")
    
    @property
    def shape(self) -> Tuple[int, ...]:
        return self._shape
    
    @property
    def dtype(self) -> str:
        return self._dtype
    
    @property
    def ndim(self) -> int:
        return len(self._shape)
    
    def __len__(self) -> int:
        return len(self._data)
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            return LazarArray(self._data[index], self._dtype)
        return self._data[index]
    
    def __setitem__(self, index, value):
        self._data[index] = value
    
    def _vector_op(self, other, op):
        if isinstance(other, (int, float)):
            result = array.array(self._data.typecode, [op(x, other) for x in self._data])
            return LazarArray(result, self._dtype)
        elif isinstance(other, LazarArray):
            if self._shape != other._shape:
                raise ValueError("Shape mismatch")
            result = array.array(self._data.typecode, [op(a, b) for a, b in zip(self._data, other._data)])
            return LazarArray(result, self._dtype)
        raise TypeError(f"Unsupported operand type(s): {type(other)}")
    
    def __add__(self, other):
        return self._vector_op(other, operator.add)
    
    def __sub__(self, other):
        return self._vector_op(other, operator.sub)
    
    def __mul__(self, other):
        return self._vector_op(other, operator.mul)
    
    def __truediv__(self, other):
        return self._vector_op(other, operator.truediv)
    
    def dot(self, other) -> Union[float, 'LazarArray']:
        if isinstance(other, LazarArray):
            if self.ndim == 1 and other.ndim == 1:
                if len(self) != len(other):
                    raise ValueError("Vectors must have same length")
                return sum(a * b for a, b in zip(self._data, other._data))
            elif self.ndim == 2 and other.ndim == 2:
                return self._matmul(other)
        raise TypeError("Dot product only supported between 1D or 2D LazarArrays")
    
    def _matmul(self, other):
        if self._shape[1] != other._shape[0]:
            raise ValueError("Matrix dimensions incompatible")
        
        m, n = self._shape
        p = other._shape[1]
        result = array.array(self._data.typecode, [0.0] * (m * p))
        
        for i in range(m):
            for k in range(n):
                if self[i*n + k] == 0:
                    continue
                for j in range(p):
                    result[i*p + j] += self[i*n + k] * other[k*p + j]
        
        return LazarArray(result, self._dtype).reshape((m, p))
    
    def reshape(self, new_shape: Tuple[int, ...]):
        total_size = math.prod(new_shape)
        if total_size != len(self._data):
            raise ValueError(f"Shape {new_shape} incompatible with array size {len(self._data)}")
        
        new_arr = LazarArray(self._data, self._dtype)
        new_arr._shape = new_shape
        return new_arr
    
    def sum(self, axis=None):
        if axis is not None:
            raise NotImplementedError("Axis parameter not yet implemented")
        return sum(self._data)
    
    def mean(self):
        if len(self._data) == 0:
            return 0.0  # atau bisa raise ValueError("Array kosong")
        return self.sum() / len(self._data)
    
    def __repr__(self):
        return f"LazarArray({list(self._data)}, dtype='{self._dtype}', shape={self._shape})"
