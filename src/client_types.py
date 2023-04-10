from typing import Any, Callable, Coroutine, Protocol, Union


class SupportsJSON(Protocol):
    def json(self) -> str:
        ...


SendFn = Callable[[Union[dict, SupportsJSON]], Coroutine[Any, Any, None]]
