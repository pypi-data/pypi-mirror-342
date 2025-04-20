# -*- coding: utf-8 -*-
import sqlite3
from typing import List, Dict, Any, Optional

# Hapus decorator @cython.cclass jika tidak diperlukan
class SQLiteHighSpeed:
    def __init__(self, path: str):
        self._conn = sqlite3.connect(path)
        self._conn.execute("PRAGMA journal_mode = WAL")
        self._conn.execute("PRAGMA synchronous = NORMAL")
        self._conn.execute("PRAGMA cache_size = -10000")

    # Hapus @cython.ccall dan sederhanakan type hints
    def fetch_fast(self, query: str, params=None) -> List[Dict]:
        if params is None:
            params = []
        cursor = self._conn.cursor()
        cursor.execute(query, params)
        cursor.row_factory = sqlite3.Row
        return [dict(row) for row in cursor]

    def bulk_insert_fast(self, table: str, columns: List[str], data: List[List[Any]]) -> None:
        placeholders = ",".join(["?"] * len(columns))
        query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
        with self._conn:
            self._conn.executemany(query, data)

    def optimize(self) -> None:
        """Defragmentasi database"""
        self._conn.execute("VACUUM")
        self._conn.execute("ANALYZE")
