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

    with Manager() as manager:
        inQ: queue.Queue[int] = manager.Queue(maxsize=5)
        ainQ: AsyncQueue[int] = AsyncQueue(inQ)
        reader : Task[int] = create_task(consumer(ainQ))
        N_process : int = 3
        count : int = 0
        work : List[int] = list(sample(range(3,7), N_process))
        print(f"{N_process} producers will put {', '.join([str(i) for i in  work])} items to the queue")
        with Pool(
            processes=N_process,
            initializer=producer_init,
            initargs=[inQ],
        ) as pool:
            results: AsyncResult = pool.map_async(producer, work) 
            pool.close()
            
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