from .highspeed.database import SQLiteHighSpeed
from .highspeed.cache import MemoryCache
from .highspeed.serializer import pack_data, unpack_data
from .highspeed.threader import ThreadPool
from .utils.memory import MemoryProfiler
from .utils.compress import compress, decompress

__version__ = "2.0.0"
__all__ = [
    'SQLiteHighSpeed',
    'MemoryCache',
    'pack_data',
    'unpack_data',
    'ThreadPool',
    'MemoryProfiler',
    'compress',
    'decompress'
]

# Optimasi import
def __getattr__(name):
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
