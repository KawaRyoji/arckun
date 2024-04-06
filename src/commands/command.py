import abc
from dataclasses import dataclass
from typing import Awaitable, Callable, Self

import discord

COMMAND_PREFIX = "$"


def parse_message(message: discord.Message) -> tuple[str, list[str]]:
    content = message.content
    splitted_contents = content.split(" ")
    command = splitted_contents.pop(0)
    return command, splitted_contents


@dataclass(frozen=True)
class Command(metaclass=abc.ABCMeta):
    name: str
    description: str
    usage: str
    process: Callable[[discord.Message], Awaitable[None]]

    async def exec(self, message: discord.Message) -> None:
        await self.process(message)

    def __str__(self) -> str:
        return f"name: {self.name}\n{self.description}\nusage: {self.usage}"


class Commands(tuple[Command, ...]):
    def map[T](self, function: Callable[[Command], T]) -> tuple[T]:
        return tuple(map(function, Self))

    def filter_with_name(self, name: str) -> Self:
        return tuple(filter(lambda c: c.name == name, self))

    def search_from_message(self, message: discord.Message) -> Command | None:
        name, _ = parse_message(message)

        if not name.startswith(COMMAND_PREFIX):
            return None

        commands = self.filter_with_name(name[1:])

        if len(commands) == 0:
            return None
        else:
            return commands[0]

    def show_all(self) -> str:
        printable_commands = self.map(lambda command: str(command))
        return "\n\n".join(printable_commands)
