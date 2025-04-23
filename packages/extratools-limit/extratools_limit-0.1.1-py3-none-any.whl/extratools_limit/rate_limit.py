import asyncio
import functools
import random
import time
from datetime import timedelta
from pathlib import Path
from typing import Any

from extratools_core.typing import PathLike


class Wait:
    def __init__(
        self,
        lockfile: PathLike | str,
        *,
        min_gap: timedelta | float = timedelta(seconds=0),
        randomness: timedelta | float = timedelta(milliseconds=1),
        use_async: bool = False,
    ) -> None:
        if isinstance(lockfile, str):
            lockfile = Path(lockfile)
        if isinstance(min_gap, timedelta):
            min_gap = min_gap.seconds
        if isinstance(randomness, timedelta):
            randomness = randomness.seconds

        self.__lockfile: PathLike = lockfile
        self.__min_gap: float = min_gap
        self.__randomness: float = randomness
        self.__use_async: bool = use_async

    def __call__(self, func):  # noqa: ANN001, ANN204
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not self.__lockfile.is_file():
                self.__lockfile.touch()

            while True:
                gap: float = time.time() - self.__lockfile.stat().st_mtime
                if (remaining_gap := self.__min_gap - gap) > 0:
                    time.sleep(remaining_gap + random.random() * self.__randomness)
                    continue

                # Note that since we are not actually locking the file,
                # there is rare chance that multiple threads can run at the same time.
                self.__lockfile.touch()
                return func(*args, **kwargs)

        @functools.wraps(func)
        async def wrapper_async(*args: Any, **kwargs: Any) -> Any:
            if not self.__lockfile.is_file():
                self.__lockfile.touch()

            while True:
                gap: float = time.time() - self.__lockfile.stat().st_mtime
                if (remaining_gap := self.__min_gap - gap) > 0:
                    await asyncio.sleep(remaining_gap + random.random() * self.__randomness)
                    continue

                # Note that since we are not actually locking the file,
                # there is rare chance that multiple threads can run at the same time.
                self.__lockfile.touch()
                return await func(*args, **kwargs)

        return wrapper_async if self.__use_async else wrapper
