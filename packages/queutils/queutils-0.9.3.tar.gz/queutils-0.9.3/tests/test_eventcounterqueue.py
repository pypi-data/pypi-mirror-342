import pytest  # type: ignore
from asyncio import (
    Task,
    create_task,
    gather,
    TimeoutError,
)
from random import choice, randint
import string
from collections import defaultdict

from queutils import EventCounterQueue


def randomword(length: int) -> str:
    """Generate a random word of fixed length"""
    # https://stackoverflow.com/a/2030081/12946084
    letters: str = string.ascii_lowercase
    return "".join(choice(letters) for i in range(length))


QSIZE: int = 10
N: int = 100  # N >> QSIZE
THREADS: int = 4
# N : int = int(1e10)


@pytest.mark.parametrize(
    "events,N, producers",
    [
        ([randomword(5) for _ in range(10)], 1000, 1),
        ([randomword(5) for _ in range(20)], 10000, 1),
        ([randomword(5) for _ in range(5)], 1000, 3),
    ],
)
@pytest.mark.timeout(10)
@pytest.mark.asyncio
async def test_1_category_counter_queue(
    events: list[str], N: int, producers: int
) -> None:
    """Test EventCounterQueue"""
    Q = EventCounterQueue(maxsize=QSIZE)

    async def producer(
        Q: EventCounterQueue, events: list[str], N: int = 100
    ) -> defaultdict[str, int]:
        """
        Test Producer for EventCounterQueue
        """
        _counter: defaultdict[str, int] = defaultdict(int)
        await Q.add_producer()
        for _ in range(N):
            cat: str = choice(events)
            count: int = randint(1, 10)
            await Q.send(cat, count)
            _counter[cat] += count
        await Q.finish()
        return _counter

    senders: list[Task] = list()

    for _ in range(producers):
        senders.append(create_task(producer(Q, events, N)))

    try:
        res_in: defaultdict[str, int] = await Q.listen()
        res_out: defaultdict[str, int] = defaultdict(int)
        for res in await gather(*senders):
            for event, count in res.items():
                res_out[event] += count

        assert res_in == res_out, f"EventCounterQueue: {res_in} != {res_out}"
        assert Q.qsize() == 0, "queue size is > 0 even it should be empty"
        assert Q.empty(), "queue not empty"
        assert Q.count == N * producers, (
            f"count returned wrong value {Q.count}, should be {N * producers}"
        )

    except TimeoutError:
        assert False, "await IterableQueue.join() failed with an empty queue finished"
