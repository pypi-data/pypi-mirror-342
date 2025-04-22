from asyncio import Queue
from typing import TypeVar
from deprecated import deprecated
from .countable import Countable
from .iterablequeue import IterableQueue, QueueDone
from collections import defaultdict
import logging

logger = logging.getLogger()
error = logger.error
message = logger.warning
verbose = logger.info
debug = logger.debug

###########################################
#
# class CounterQueue
#
###########################################
T = TypeVar("T")


@deprecated(version="0.9.1", reason="Use EventCounterQueue instead")
class CounterQueue(Queue[T], Countable):
    """
    CounterQueue is a asyncio.Queue for counting items
    """

    _counter: int
    _count_items: bool
    _batch: int

    def __init__(
        self, *args, count_items: bool = True, batch: int = 1, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self._counter = 0
        self._count_items = count_items
        self._batch = batch

    def task_done(self) -> None:
        super().task_done()
        if self._count_items:
            self._counter += 1
        return None

    @property
    def count(self) -> int:
        """Return number of completed tasks"""
        return self._counter * self._batch

    @property
    def count_items(self) -> bool:
        """Whether or not count items"""
        return self._count_items


class EventCounterQueue(IterableQueue[tuple[str, int]]):
    """
    EventCounterQueue is a asyncio.Queue for counting events by name
    """

    _counter: defaultdict[str, int]
    _batch: int

    def __init__(self, *args, batch: int = 1, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._batch = batch
        self._counter = defaultdict(int)

    async def receive(self) -> tuple[str, int]:
        """Receive an event value from the queue and sum it"""
        event: str
        value: int
        event, value = await super().get()
        self._counter[event] += value
        super().task_done()
        return (event, value)

    async def send(self, event: str = "count", value: int = 1) -> None:
        """Send count of an event"""
        await super().put((event, value))
        return None

    def get_count(self, event: str = "count") -> int:
        """Return count for an event"""
        return self._counter[event]

    def get_counts(self) -> defaultdict[str, int]:
        """Return counts of all events"""
        return self._counter

    async def listen(self) -> defaultdict[str, int]:
        """Listen for event values"""
        try:
            while True:
                await self.receive()
        except QueueDone:
            pass
        return self.get_counts()


class QCounter:
    def __init__(self, Q: Queue[int]):
        self._count = 0
        self._Q: Queue[int] = Q

    @property
    def count(self) -> int:
        return self._count

    async def start(self) -> None:
        """Read and count items from Q"""
        while True:
            self._count += await self._Q.get()
            self._Q.task_done()
