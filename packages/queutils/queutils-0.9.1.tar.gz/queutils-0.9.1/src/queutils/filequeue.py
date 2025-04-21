# -----------------------------------------------------------
#  Class FileQueue(asyncio.Queue)
#
#  Class to build asyncio.Queue of filename (pathlib.Path) based on arguments given.
#  - Inherits from queutils.IterableQueue
#  - Supports include/exclude filters
#
# -----------------------------------------------------------

__author__ = "Jylpah"
__copyright__ = "Copyright 2024, Jylpah <Jylpah@gmail.com>"
__credits__ = ["Jylpah"]
__license__ = "MIT"
# __version__ = "1.0"
__maintainer__ = "Jylpah"
__email__ = "Jylpah@gmail.com"
__status__ = "Production"


import logging

# from asyncio import Queue
import aioconsole  # type: ignore
from fnmatch import fnmatch, fnmatchcase
from pathlib import Path
from typing import Optional, Sequence

from .iterablequeue import IterableQueue

logger = logging.getLogger(__name__)
error = logger.error
message = logger.warning
verbose = logger.info
debug = logger.debug


def str2path(filename: str | Path, suffix: str | None = None) -> Path:
    """
    Convert filename (str) to pathlib.Path
    """
    if isinstance(filename, str):
        filename = Path(filename)
    if suffix is not None and not filename.name.lower().endswith(suffix):
        filename = filename.with_suffix(suffix)
    return filename


class FileQueue(IterableQueue[Path]):
    """
    Class to create a IterableQueue(asyncio.Queue) of filenames based on 
    given directories and files as arguments. 
    Supports include/exclude filters based on filenames.
    """

    def __init__(
        self,
        base: Optional[Path] = None,
        filter: str = "*",
        exclude: bool = False,
        case_sensitive: bool = True,
        follow_symlinks: bool = False, 
        **kwargs,
    ):
        assert base is None or isinstance(base, Path), "base has to be Path or None"
        assert isinstance(filter, str), "filter has to be string"
        assert isinstance(case_sensitive, bool), "case_sensitive has to be bool"
        assert isinstance(follow_symlinks, bool), "follow_symlinks has to be bool"
        
        # debug(f"maxsize={str(maxsize)}, filter='{filter}'")
        super().__init__(count_items=True, **kwargs)
        self._base: Optional[Path] = base
        # self._done: bool = False
        self._case_sensitive: bool = False
        self._exclude: bool = False
        self._follow_symlinks : bool = follow_symlinks
        self.set_filter(filter=filter, exclude=exclude, case_sensitive=case_sensitive)

    def set_filter(
        self,
        filter: str = "*",
        exclude: bool = False,
        case_sensitive: bool = False,
    ):
        """set filtering logic. Only set (!= None) params are changed"""
        assert isinstance(case_sensitive, bool), "case_sensitive must be type of bool"
        assert isinstance(exclude, bool), "exclude must be type of bool"

        self._case_sensitive = case_sensitive
        self._exclude = exclude
        self._filter = filter
        debug(
            "filter=%s exclude=%s, case_sensitive=%s",
            str(self._filter),
            self._exclude,
            self._case_sensitive,
        )

    async def mk_queue(self, files: Sequence[str | Path]) -> bool:
        """Create file queue from arguments given
        '-' denotes for STDIN
        """
        assert files is not None and len(files) > 0, "No files given to process"
        await self.add_producer()
        path: Path
        file: str | Path
        try:
            if isinstance(files[0], str) and files[0] == "-":
                stdin, _ = await aioconsole.get_standard_streams()
                while (line := await stdin.readline()) is not None:
                    path = Path(line.decode("utf-8").removesuffix("\n"))
                    if self._base is not None:
                        path = self._base / path
                    await self.put(path)
            else:
                for file in files:
                    path = str2path(file)
                    if self._base is not None:
                        path = self._base / path
                    await self.put(path)
        except Exception as err:
            error(f"{err}")
        return await self.finish()


    async def put(self, path: Path) -> None:
        """Recursive function to build process queue. Sanitize filename"""
        assert isinstance(path, Path), "path has to be type Path()"
        try:
            if path.is_symlink() and not self._follow_symlinks:
                return None
            if path.is_dir():
                for child in path.iterdir():
                    await self.put(child)
            elif path.is_file() and self.match(path):
                debug("Adding file to queue: %s", str(path))
                await super().put(path)
        except Exception as err:
            error(f"{err}")
        return None

    def match(self, path: Path) -> bool:
        """ "Match file name with filter

        https://docs.python.org/3/library/fnmatch.html
        """
        assert isinstance(path, Path), "path has to be type Path()"
        try:
            m: bool
            if self._case_sensitive:
                m = fnmatch(path.name, self._filter)
            else:
                m = fnmatchcase(path.name, self._filter)
            return m != self._exclude
        except Exception as err:
            error(f"{err}")
        return False
