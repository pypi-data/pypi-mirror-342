import zlib

def compress(data: bytes, level: int = 9) -> bytes:
    """Kompresi data dengan zlib (level 1-9)."""
    return zlib.compress(data, level)

def decompress(data: bytes) -> bytes:
    """Dekompresi data."""
    return zlib.decompress(data)
