import abc
from dataclasses import dataclass
from typing import Awaitable, Callable, Self

import discord

from ..utils import Result


def parse_message(message: discord.Message) -> tuple[str, tuple[str, ...]]:
    content = message.content
    splitted_contents = content.split(" ")
    command = splitted_contents.pop(0)
    return command, tuple(splitted_contents)


@dataclass(frozen=True)
class Command(metaclass=abc.ABCMeta):
    name: str
    description: str
    usage: str
    process: Callable[[tuple[str, ...]], Awaitable[Result[str, str]]]

    async def exec(self, *args: str) -> Result[str, str]:
        return await self.process(*args)

    def __str__(self) -> str:
        return f"\n## {self.name}\n\n{self.description}\n使い方：`{self.usage}`"


class Commands(tuple[Command, ...]):
    def is_empty(self) -> bool:
        return len(self) == 0

    def map[T](self, function: Callable[[Command], T]) -> tuple[T]:
        return tuple(map(function, self))

    def filter(self, function: Callable[[Command], bool]) -> Self:
        return Commands(filter(function, self))

    def search_from_name(self, name: str) -> Command | None:
        commands = self.filter(lambda c: c.name == name)

        if self.is_empty():
            return None
        else:
            return commands[0]

    def show_all(self) -> str:
        printable_commands = self.map(lambda command: str(command))
        return "\n".join(printable_commands)
