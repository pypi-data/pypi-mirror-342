from asyncio import sleep, run, TaskGroup
from random import random
from queutils import IterableQueue, QueueDone
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
