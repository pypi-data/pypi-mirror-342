# FileQueue

`FileQueue` builds a queue (`IterableQueue[pathlib.Path]`) of the matching files found based on search parameters given. It can search both list of files or directories or mixed. Async method `FileQueue.mk_queue()` searches subdirectories of given directories.  

## Features

- Input can be given both as `str` and `pathlib.Path`
- `exclude: bool` exclusive or  inclusive filtering. Default is `False`.
- `case_sensitive: bool` case sensitive filtering (use of `fnmatch` or `fnmatchcase`). Default is `True`.
- `follow_symlinks: bool` whether to follow symlinks. Default is `False`.

# Example

```python
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
    
    # test whether FileQueue.mk_queue() Task is finished
    if spider.done():
        print("finished, no need to use fileQ.join()")
    else:
        print("Oops, it did not work as promised")

if __name__ == "__main__":
    run(main())
```