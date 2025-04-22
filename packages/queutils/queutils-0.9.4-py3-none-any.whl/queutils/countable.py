

from typing import Protocol

class Countable(Protocol):
    """"
    Protocol interface for count @property
    """
    @property
    def count(self) -> int:
        ...
