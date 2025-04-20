# Javapy - High-Performance Python Utilities 🚀

**Versi:** 2.0.1  
**Penulis:** Eternals  
**Email:** eternals.tolong@gmail.com  
**GitHub:** [Eternals-Satya/javapy](https://github.com/Eternals-Satya/javapy)  

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![PyPI](https://img.shields.io/pypi/v/javapy)

## 📦 Deskripsi Paket
Javapy adalah paket Python berkinerja tinggi yang menyediakan berbagai utilitas untuk:
- Akses database super cepat dengan optimasi SQLite3
- Caching in-memory dengan manajemen TTL
- Serialisasi data biner efisien
- Multi-threading aman

Dibangun dengan:
- **Cython** untuk kecepatan setara C
- **Pure Python** tanpa dependensi eksternal
- Kompatibel dengan **Termux** dan platform lain

## 🔥 Fitur Unggulan
### 1. Database High-Speed
```python
from javapy import SQLiteHighSpeed

db = SQLiteHighSpeed(":memory:")
db.bulk_insert_fast("users", ["name", "age"], [["Budi", 25], ["Ani", 30]])
print(db.fetch_fast("SELECT * FROM users"))
```

### 2. Memory Cache
```python
from javapy import MemoryCache

cache = MemoryCache()
cache.set("user:1", {"nama": "Budi", "saldo": 1000000}, ttl=60)  # Expires in 60s
print(cache.get("user:1"))
```

### 3. Binary Serializer
```python
from javapy import pack_data, unpack_data

data = {"user": {"id": 1, "active": True}}
binary = pack_data(data)  # Serialize ke bytes
print(unpack_data(binary))  # Deserialize kembali
```

## 🛠️ Instalasi
### Via Pip
```bash
pip install javapy
```

### Manual Build (Untuk Termux/ARM)
```bash
git clone https://github.com/Eternals-Satya/javapy.git
cd javapy
pip install -e .
```

## 📚 Dokumentasi Lengkap
### 1. SQLiteHighSpeed
| Method | Parameter | Contoh |
|--------|-----------|--------|
| `fetch_fast` | `query: str`, `params: list` | `db.fetch_fast("SELECT * FROM users WHERE age > ?", [25])` |
| `bulk_insert_fast` | `table: str`, `columns: list`, `data: list[list]` | `db.bulk_insert_fast("users", ["name"], [["Budi"], ["Ani"]])` |
| `optimize` | - | `db.optimize()` |

### 2. MemoryCache
```python
cache = MemoryCache()
cache.set("key", value, ttl=60)  # TTL dalam detik
cache.get("key")  # Return None jika expired
cache.purge()  # Bersihkan yang expired
```

### 3. Thread Pool
```python
from javapy import ThreadPool

def task(name):
    print(f"Hello {name}")

pool = ThreadPool(max_workers=4)
pool.submit(task, "Budi")
pool.wait_completion()
```

## ⚡ Benchmark
| Operasi | Kecepatan | Catatan |
|---------|-----------|---------|
| Bulk Insert 10k data | ~0.8 detik | Dengan WAL mode |
| Cache read/write | ~0.0001 detik/op | In-memory |
| Binary serialization | 2x lebih cepat dari pickle | Untuk data kecil |

### "Platform not supported"
Untuk Termux/ARM, gunakan:
```bash
python -m build --sdist
pip install dist/javapy-2.0.0.tar.gz
```

## 🤝 Berkontribusi
1. Fork repository
2. Buat branch baru (`git checkout -b fitur-baru`)
3. Commit perubahan (`git commit -m 'Tambahkan fitur'`)
4. Push ke branch (`git push origin fitur-baru`)
5. Buat Pull Request

## 📜 Lisensi
MIT License - Bebas digunakan untuk proyek komersil maupun open source

---
**💡 Tips:** Untuk performa maksimal di Termux, jalankan dengan `taskset`:
```bash
taskset -c 0 python script.py
```
