# AsyncQueue

`AsyncQueue` is a async wrapper for non-async `queue.Queue`. It can be used to create 
an `asyncio.Queue` compatible out of a (non-async) `multiprocessing.Queue`. This is handy to have `async` code running in `multiprocessing` processes and yet be able to communicate with the parent via (non-async) managed `multiprocessing.Queue` queue. 


## Features 

- `asyncio.Queue` compatible
- `queue.Queue` support
- `multiprocessing.Queue` support
  
## Example

### Create async wrapper

```python
import queue
from queutils import AsyncQueue

syncQ: queue.Queue[int] = queue.Queue(maxsize=5)
asyncQ: AsyncQueue[int] = AsyncQueue(syncQ)

# asyncQ can not be used as any asyncio.Queue
```

### Full example

Below is example code where a `multiprocessing.Manager.queue` is used to communicate between three child producer processes and a parent process that reads the queue. The code in both the parent and the child processes is `async`.

```python
from multiprocessing import Manager
from multiprocessing.pool import Pool, AsyncResult
from queutils import AsyncQueue
import queue
from asyncio import run, sleep, CancelledError, create_task, Task, gather
import asyncio
from random import random, sample
from typing import List
from time import time

start : float = time()

def since() -> float:
    return time() - start

asyncQ : AsyncQueue

async def main() -> None:
    """
    Creates a multiprocessing.pool.Pool inside a multiprocessing.Manager() context manager and 
    uses multiprocessing.Manager.Queue() to communicate between the parent process (consumer) 
    and three child processes (producers). 
    """

    with Manager() as manager:
        inQ: queue.Queue[int] = manager.Queue(maxsize=5)
        ainQ: AsyncQueue[int] = AsyncQueue(inQ)
        reader : Task[int] = create_task(consumer(ainQ))
        N_process : int = 3
        count : int = 0
        work : List[int] = list(sample(range(3,7), N_process))
        print(f"work to do {work}")
        with Pool(
            processes=N_process,
            initializer=producer_init,
            initargs=[inQ],
        ) as pool:
            results: AsyncResult = pool.map_async(producer, work) 
            pool.close()
            
            # wait the child processes to finish
            while not results.ready():
                await sleep(0.2)
                print(f"{since():.3f} waiting")
            await ainQ.join()
            reader.cancel()

            for res in results.get():
                count += res

        print(f"{since():.3f} :: {N_process} producers added {count} items to the queue")
        reader_count : int = 0
        for res in await gather(*[reader]):
            reader_count += res
        print(f"{since():.3f} :: reader read {reader_count} items from the queue")


def  producer_init(outQ: queue.Queue[int]):
    """
    multiprocessing init function to assing the created AsyncQueue to a global variable that is 
    then available in the forked child process
    """
    global asyncQ
    asyncQ = AsyncQueue(outQ)


def producer(N :int) -> int:
    return run(producer_async(N), debug=True)

async def  producer_async(N: int) -> int:
    """
    async function to add N items to the shared queue
    """
    global asyncQ
    count : int = 0
    for i in range(N):
        await sleep(0.1 * random())   
        await asyncQ.put(i)
        print(f"{since():.3f} put {i} to the queue")
        count += 1
    return count

async def consumer(inQ: asyncio.queues.Queue[int]) -> int:
    """
    Async consumer of an async queue 
    """
    try:
        count : int = 0
        while True:
            await sleep(0.1 * random())
            print(f"{since():.3f} awating to read the queue")
            i : int =  await inQ.get()
            print(f"{since():.3f} read {i} from the queue")
            count += 1
    except CancelledError:
        pass
    return count

if __name__ == "__main__":
    run(main())
```

## Results

```bash
% python asyncqueue_demo.py                                                                queutils/demos
3 producers will put 3, 6, 4 items to the queue
0.039 awating to read the queue
0.089 put 0 to the queue
0.092 read 0 from the queue
0.100 put 0 to the queue
0.108 put 0 to the queue
0.108 put 1 to the queue
0.155 put 1 to the queue
0.158 put 2 to the queue
0.192 awating to read the queue
0.193 read 0 from the queue
0.196 put 3 to the queue
0.203 awating to read the queue
0.203 read 0 from the queue
0.210 waiting
0.210 put 1 to the queue
0.285 awating to read the queue
0.286 read 1 from the queue
0.293 put 2 to the queue
0.348 awating to read the queue
0.349 read 1 from the queue
0.350 put 3 to the queue
0.411 waiting
0.425 awating to read the queue
0.426 read 2 from the queue
0.427 put 2 to the queue
0.466 awating to read the queue
0.466 read 3 from the queue
0.475 put 4 to the queue
0.486 awating to read the queue
0.486 read 1 from the queue
0.521 awating to read the queue
0.522 read 2 from the queue
0.539 awating to read the queue
0.540 read 3 from the queue
0.567 put 5 to the queue
0.613 waiting
0.634 awating to read the queue
0.634 read 2 from the queue
0.655 awating to read the queue
0.655 read 4 from the queue
0.690 awating to read the queue
0.691 read 5 from the queue
0.697 :: 3 producers added 13 items to the queue
0.697 :: reader read 13 items from the queue
```