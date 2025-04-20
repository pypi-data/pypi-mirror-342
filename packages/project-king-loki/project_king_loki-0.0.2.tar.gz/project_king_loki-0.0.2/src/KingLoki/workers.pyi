"""workers [`Module`].

Contains tools to create and manage slave workers as efficiently as
possible.
"""

from concurrent.futures import Future
from typing import Callable, Union, Literal
from typing import Any, Self

class Workers:
    """A compact worker thread dispatcher designed for efficiency
    and speed.
    
    Dispatches any given number of worker threads at the caller's
    disposal. Once tasks are handed off, any idle thread will pick
    up the task and completes it.
    """

    def __init__(self, wcount: int = ...) -> None:
        """Create worker thread dispatcher with `wcount` works."""

    def handoff_(self, ID: str, function: Callable[..., Any], *functionArguments: object) -> Future:
        """Adds a job to the queue, to be picked up by an idle worker."""

    def noerror_(self, ID: str, timeout: float = ...) -> bool:
        """Returns `True` if the task completed without error else `False`."""

    def checkup_(self, ID: str, wait=False, timeout: float = ...) -> Union[Literal['__failed__','__timeout__'], Any, None]:
        """Returns the result of the job if completed successfully. Returns `'__failed__'` if the job failed.
        Returns `'__timeout__'` if timeout is set and has reached. Else returns None."""

    def evict_(self, wait=False, timeout: float = ...) -> None:
        """Evicts all workers and marks all tasks as completed."""

    def __call__(self, wait=False, timeout: float = ...) -> None:
        """Sets the eviction parameters. Meant to be called as the last statment before the
        `with` statement ends."""

    def __enter__(self) -> Self: ...
    def __exit__(self, *args, **kwargs) -> bool: ...