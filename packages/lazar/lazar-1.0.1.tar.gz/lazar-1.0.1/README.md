# README.md Lengkap untuk Lazar

```markdown
# Lazar

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Lazar adalah paket Python ringan yang menyediakan fungsionalitas mirip NumPy dan Transformers, tetapi diimplementasikan murni dalam Python tanpa dependensi eksternal. Dibangun untuk kasus penggunaan dimana instalasi paket berat tidak memungkinkan atau tidak diinginkan.

## Fitur Utama

- **Komputasi Numerik Efisien**
  - Array multidimensi dengan operasi vektorisasi
  - Operasi aljabar linear (dot product, matmul)
  - Fungsi matematika dasar (exp, log, sin, cos, sqrt)

- **Pemrosesan Bahasa Alami**
  - Tokenizer cepat dengan dukungan special tokens
  - Model bahasa sederhana dengan embeddings
  - Preprocessing teks dasar

- **Optimasi Performa**
  - Manajemen memori efisien dengan `array.array`
  - Operasi batch dan lazy evaluation
  - Sistem benchmarking terintegrasi

## Instalasi

Lazar tersedia di PyPI dan dapat diinstall menggunakan pip:

```bash
pip install lazar
```


## Penggunaan Cepat

### Operasi Array

```python
from lazar import LazarArray, exp

# Membuat array
a = LazarArray([1, 2, 3])
b = LazarArray([4, 5, 6])

# Operasi dasar
c = a + b
d = a.dot(b)

# Fungsi matematika
e = exp(a)

# Reshape array
matrix = LazarArray(range(9)).reshape((3, 3))
```

### Pemrosesan Teks

```python
from lazar.nl import LazarTokenizer

# Inisialisasi tokenizer
tokenizer = LazarTokenizer()
tokenizer.fit(["Hello world!", "This is a test sentence."])

# Encode/decode teks
encoded = tokenizer.encode("Hello test")
decoded = tokenizer.decode(encoded)
```

### Benchmarking

```python
from lazar.utils import benchmark, compare_with_numpy

@benchmark
def compute_operations(a, b):
    return (a + b) * (a - b)

# Bandingkan dengan NumPy
result = compare_with_numpy(
    lambda x, y: x.dot(y),
    lambda x, y: x.dot(y),  # Fungsi NumPy
    LazarArray([1, 2, 3]),
    LazarArray([4, 5, 6])
)
```

## Dokumentasi Lengkap

### Array Operations

- `LazarArray(data, dtype='float64')`: Membuat array baru
- `reshape(new_shape)`: Mengubah bentuk array
- `dot(other)`: Perkalian dot product
- `sum()`: Penjumlahan elemen

### Mathematical Functions

- `exp(arr)`: Exponential
- `log(arr)`: Natural logarithm
- `sin(arr)`, `cos(arr)`: Trigonometri
- `sqrt(arr)`: Square root

### NLP Module

- `LazarTokenizer()`: Tokenizer teks
  - `fit(texts)`: Membangun vocabulary
  - `encode(text)`: Konversi teks ke token IDs
  - `decode(ids)`: Konversi token IDs ke teks
- `LazarLanguageModel(vocab_size)`: Model bahasa sederhana
  - `embed(token_ids)`: Membuat word embeddings
  - `predict_next_token(embeddings)`: Prediksi token berikutnya

## Requirements

Lazar dirancang untuk bekerja dengan Python standar tanpa dependensi eksternal. Namun untuk pengembangan dan testing, beberapa paket tambahan diperlukan:

### `requirements.txt`

```
# Untuk pengembangan
black==22.3.0
flake8==4.0.1
mypy==0.942
pytest==7.1.2

# Opsional untuk benchmarking
numpy==1.22.3
```

## Lisensi

Lazar dirilis di bawah lisensi MIT. Lihat [LICENSE](LICENSE) untuk detail lengkap.

## Dukungan

Untuk masalah atau pertanyaan, silakan buka [issue](https://github.com/Eternals-Satya/lazar/issues) di repository GitHub.

