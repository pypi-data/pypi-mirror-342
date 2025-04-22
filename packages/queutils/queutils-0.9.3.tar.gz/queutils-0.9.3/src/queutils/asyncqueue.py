# -----------------------------------------------------------
#  Class AsyncQueue(asyncio.Queue, Generic[T])
#
#  asyncio wrapper for non-async queue.Queue. Can be used to create
#  an asyncio.Queue out of a (non-async) multiprocessing.Queue.
#
# -----------------------------------------------------------

__author__ = "Jylpah"
__copyright__ = "Copyright 2024, Jylpah <Jylpah@gmail.com>"
__credits__ = ["Jylpah"]
__license__ = "MIT"
__maintainer__ = "Jylpah"
__email__ = "Jylpah@gmail.com"
__status__ = "Production"


from queue import Full, Empty, Queue
from asyncio.queues import QueueEmpty, QueueFull
import asyncio
from typing import Generic, TypeVar
import logging
from asyncio import sleep

T = TypeVar("T")

logger = logging.getLogger(__name__)

debug = logger.debug
message = logger.warning
verbose = logger.info
error = logger.error


class AsyncQueue(asyncio.Queue, Generic[T]):
    """
    Async wrapper for non-async queue.Queue. Can be used to create
    an asyncio.Queue out of a (non-async) multiprocessing.Queue.
    """

    def __init__(self, queue: Queue[T], asleep: float = 0.001):
        self._Q: Queue[T] = queue
        # self._maxsize: int = queue.maxsize
        self._done: int = 0
        self._items: int = 0
        self._sleep: float = asleep

    @property
    def maxsize(self) -> int:
        """not supported by queue.Queue"""
        return self._Q.maxsize

    async def get(self) -> T:
        while True:
            try:
                return self.get_nowait()
            except QueueEmpty:
                await sleep(self._sleep)

    def get_nowait(self) -> T:
        try:
            return self._Q.get_nowait()
        except Empty:
            raise QueueEmpty

    async def put(self, item: T) -> None:
        while True:
            try:
                return self.put_nowait(item)
            except QueueFull:
                await sleep(self._sleep)

    def put_nowait(self, item: T) -> None:
        try:
            self._Q.put_nowait(item)
            self._items += 1
            return None
        except Full:
            raise QueueFull

    async def join(self) -> None:
        while True:
            if self._Q.empty():
                return None
            else:
                await sleep(self._sleep)

    def task_done(self) -> None:
        self._Q.task_done()
        self._done += 1
        return None

    def qsize(self) -> int:
        return self._Q.qsize()

    @property
    def done(self) -> int:
        """Number of done items"""
        return self._done

    @property
    def items(self) -> int:
        """Number of items ever put to the queue"""
        return self._items

    def empty(self) -> bool:
        return self._Q.empty()

    def full(self) -> bool:
        return self._Q.full()
