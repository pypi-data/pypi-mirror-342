# IterableQueue

`IterableQueue` is an `asyncio.Queue` subclass that is `AsyncIterable[T]` i.e. it can be 
iterated in `async for` loop. The great benefit of `IterableQueue` is that it terminates automatically when the queue has been filled and emptied. This simplifies more complex queue-based processing flows.
    
## Features

- `asyncio.Queue` interface
- `AsyncIterable` support: `async for item in queue:`
- Automatic termination of the consumers with `QueueDone` exception when the queue has been emptied 
- Producers must be registered with `add_producer()` and they must notify the queue
  with `finish()` once they have finished adding items 
- Countable interface to count number of items task_done() through `count` property
- Countable property can be disabled with count_items=False. This is useful when you
    want to sum the count of multiple IterableQueues 

### Experimental

- `Asyncio.Queue` `_nowait()` methods are experimental, but "seem to work" in test pipeline


## Examples

### Producers fill a queue

A *Producer* is "process" that adds items to the queue. A producer needs to be registered to the queue with `add_producer()` coroutine. Once a producer has added all the items it intends to, it notifies the queue with `finish()`

```python
from queutils.iterablequeue import IterableQueue

async def producer(
    Q: IterableQueue[int], N: int
) -> None:

    # Add a producer to add items to the queue
    await Q.add_producer()
    
    for i in range(N):
        await Q.put(i)
    
    # notify the queue that this producer does not add more
    await Q.finish()
    
    return None
```

### Consumers take items from the queue

*Consumer* is a "process" that takes items from a queue with `get()` coroutine. Since `IterableQueue` is `AsyncIterable`, it can be iterated over `async for`.

```python
from queutils.iterablequeue import IterableQueue

async def consumer(Q: IterableQueue[int]):
    """
    Consume the queue
    """
    async for i in Q:
        print(f"consumer: got {i} from the queue")        
    print(f"consumer: queue is done")
```

###  Complete example 

A `IterableQueue` example with multiple producers and consumers. This works with Python 3.11 and higher since the use of `asyncio.TaskGroup`.  

```python
## Python 3.11+ required 

from asyncio import sleep, run, TaskGroup
from random import random
from queutils.iterablequeue import IterableQueue, QueueDone
from time import time

start : float = time()

def since() -> float:
    return time() - start

async def producer(
    Q: IterableQueue[int], N: int, id: int
) -> None:
    """
    Fill the queue with N items
    """
    await Q.add_producer()
    try:
        for i in range(N):
            await sleep(0.5 * random())
            print(f"{since():.2f} producer {id}: awaiting to put {i} to queue")
            await Q.put(i)
            print(f"{since():.2f} producer {id}: put {i} to queue")
        await Q.finish()
    except QueueDone:
        print(f"ERROR: producer {id}, this should not happen")
    return None

async def consumer(Q: IterableQueue[int], id: int = 1):
    """
    Consume the queue
    """
    async for i in Q:
        print(f"{since():.2f} consumer {id}: got {i} from queue")
        await sleep(0.5 * random())
    print(f"{since():.2f} consumer {id}: queue is done")

async def main() -> None:
    """
    Create a queue with maxsize and have multiple producers to fill it and 
    multiple consumers to consume it over async for loop
    """
    queue : IterableQueue[int] = IterableQueue(maxsize=5)

    async with TaskGroup() as tg:
        for i in range(1,3):
            tg.create_task(producer(Q=queue, N=5, id=i))
        await sleep(2)
        for  i in range(1,4):
            tg.create_task(consumer(Q=queue, id=i))

if __name__ == "__main__":
    run(main())

```