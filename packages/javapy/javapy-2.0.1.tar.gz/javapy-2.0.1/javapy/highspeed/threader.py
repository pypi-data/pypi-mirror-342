import threading
from queue import Queue
from typing import Callable, Any

class ThreadPool:
    def __init__(self, max_workers: int = 4):
        self.tasks = Queue()
        self.workers = [
            threading.Thread(
                target=self._worker,
                daemon=True
            ) for _ in range(max_workers)
        ]
        for w in self.workers:
            w.start()

    def _worker(self) -> None:
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                func(*args, **kwargs)
            finally:
                self.tasks.task_done()

    def submit(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        """Submit task ke thread pool."""
        self.tasks.put((func, args, kwargs))

    def wait_completion(self) -> None:
        """Block sampai semua task selesai."""
        self.tasks.join()
