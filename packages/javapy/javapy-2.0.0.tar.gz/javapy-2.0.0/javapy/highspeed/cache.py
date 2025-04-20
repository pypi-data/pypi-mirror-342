import cython
from time import time
from typing import Any, Dict, Optional

@cython.cclass
class MemoryCache:
    _store: dict
    _ttl: dict
    
    def __init__(self):
        self._store = {}
        self._ttl = {}

    @cython.ccall
    def set(self, key: str, value: Any, ttl: int = 60) -> None:
        self._store[key] = value
        self._ttl[key] = time() + ttl

    @cython.ccall
    def get(self, key: str) -> Optional[Any]:
        if key in self._store and time() < self._ttl.get(key, 0):
            return self._store[key]
        return None

    @cython.ccall
    def purge(self) -> None:
        current = time()
        expired = [k for k, v in self._ttl.items() if v < current]
        for k in expired:
            del self._store[k]
            del self._ttl[k]

    @cython.ccall
    def clear(self) -> None:
        """Bersihkan seluruh cache"""
        self._store.clear()
        self._ttl.clear()
