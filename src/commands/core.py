import abc
from dataclasses import dataclass
from typing import Callable, Self

import discord

from ..utils import Failure, Result, Success

COMMAND_PREFIX = "$"  # コマンドメッセージのプレフィックス


def parse_message(message: discord.Message) -> tuple[str, tuple[str, ...]]:
    content = message.content
    splitted_contents = content.split(" ")
    command = splitted_contents.pop(0)
    return command, tuple(splitted_contents)


@dataclass(frozen=True)
class Command[S, F](metaclass=abc.ABCMeta):
    name: str
    description: str
    usage: str

    @abc.abstractmethod
    async def exec(self, *args: str) -> Result[S, F]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def response(self, result: Result[S, F], message: discord.Message) -> None:
        raise NotImplementedError()

    def __str__(self) -> str:
        return f"## {self.name}\n{self.description}\n使い方：`{self.usage}`"


class Commands(tuple[Command, ...]):
    def is_empty(self) -> bool:
        return len(self) == 0

    def map[T](self, function: Callable[[Command], T]) -> tuple[T]:
        return tuple(map(function, self))

    def filter(self, function: Callable[[Command], bool]) -> Self:
        return Commands(filter(function, self))

    def search_from_name(self, name: str) -> Command | None:
        commands = self.filter(lambda c: c.name == name)

        if commands.is_empty():
            return None
        else:
            return commands[0]

    def show_all(self) -> str:
        printable_commands = self.map(lambda command: str(command))
        return "\n".join(printable_commands)


async def response_using_text_message(
    result: Result[str, str], message: discord.Message, usage: str
) -> None:
    match result:
        case Success():
            await message.reply(result.value)
        case Failure():
            await message.reply(result.value + "\n使い方：`" + usage + "`")
