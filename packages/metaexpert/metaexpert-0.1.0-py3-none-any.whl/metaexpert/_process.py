from typing import Any, Callable, Coroutine

from logger import get_logger, Logger


class Process:
    def __init__(self, name) -> None:
        self.name: str = name
        self.logger: Logger = get_logger(__name__)

    def on_init(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    def on_deinit(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    def on_trade(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    def on_transaction(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    # def on_tick(self, func: Callable[[], None]) -> Callable[[], Coroutine[Any, Any, None]]:
    def on_tick(self, func: Callable) -> Callable:
        def inner(*args, **kwargs) -> None:
            # task = asyncio.create_task(func())
            # task
            func(*args, **kwargs)
            # await self.__tick()
            # task = asyncio.create_task(self.__tick())
            # await task
            # i = 3
            # while i > 0:
            #     func()
            #     print(self, " ", i)
            #     i -= 1
            # return func()

        return inner

    # Call: TypeAlias = Callable[[list[Any], dict[str, Any]], None]

    def on_bar(self, time_frame: str = "1h") -> Callable:
        def outer(
                func: Callable[[tuple[Any, ...], dict[str, Any]], None],
        ) -> Callable[[tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, None]]:
            # def inner(*args, **kwargs) -> None:
            #     func(*args, **kwargs)
            #     print(time_frame)

            async def async_inner(*args, **kwargs) -> None:
                await func(*args, **kwargs)

            return async_inner

        return outer

    def on_timer(self, interval: int = 1000) -> Callable:
        """Decorator for timer-based event handling.

        Args:
            interval (int, optional): Time interval in milliseconds. Defaults to 1000.

        Returns:
            Callable: Decorated function that executes at specified intervals.
        """

        def outer(func: Callable) -> Callable:
            def inner() -> None:
                func()
                print(interval)

            return inner

        return outer

    def on_book(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner
