from queutils import FileQueue
from pathlib import Path
from asyncio import Task, create_task, run

async def main() -> None:
    fileQ = FileQueue(filter="*.py",  case_sensitive=False)
    current_dir = Path(__file__).parent
    spider : Task = create_task(fileQ.mk_queue(files=[current_dir]))
    async for filename in fileQ:
        try:
            rel_path : Path = filename.relative_to(current_dir)
            print(f"found {rel_path}")
        except ValueError as err:
            print(f"{err}")
    
    if spider.done():
        print("finished, no need to use fileQ.join()")
    else:
        print("Oops, it did not work as promised")

if __name__ == "__main__":
    run(main())