import tracemalloc

class MemoryProfiler:
    def __init__(self):
        tracemalloc.start()

    def snapshot(self) -> str:
        """Ambil snapshot memory usage."""
        current, peak = tracemalloc.get_traced_memory()
        return f"Current: {current / 1024:.2f} KB | Peak: {peak / 1024:.2f} KB"

    def reset(self) -> None:
        """Reset profiler."""
        tracemalloc.stop()
        tracemalloc.start()
