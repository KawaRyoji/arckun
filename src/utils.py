from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Success[T]:
    value: T


@dataclass(frozen=True)
class Failure[E]:
    value: E


type Result[T, E] = Success[T] | Failure[E]


def use_state[T](init: T) -> tuple[Callable[[], T], Callable[[T], None]]:
    state = init

    def set_state(s: T) -> None:
        nonlocal state
        state = s

    def get_state() -> None:
        return state

    return get_state, set_state
