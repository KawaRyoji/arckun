from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Callable

import discord

COMMAND_PREFIX = "$"  # コマンドメッセージのプレフィックス


def parse_message(message: discord.Message) -> tuple[str, tuple[str, ...]] | None:
    content = message.content
    if not content.startswith(COMMAND_PREFIX):
        return None
    splitted_contents = content.split(" ")
    command = splitted_contents.pop(0)
    return command[1:], tuple(splitted_contents)


@dataclass(frozen=True)
class Command(metaclass=abc.ABCMeta):
    name: str
    description: str
    usage: str

    @abc.abstractmethod
    def exec(self, source_message: discord.Message, *args: str) -> Response:
        raise NotImplementedError()

    def __str__(self) -> str:
        return f"## {self.name}\n{self.description}\n使い方：`{self.usage}`"


@dataclass(frozen=True)
class Response:
    content: str | None
    embed: discord.Embed | None = None
    view: discord.ui.View | None = None
    delete_after: float | None = None

    async def send(self, source_message: discord.Message) -> None:
        await source_message.reply(
            content=self.content,
            embed=self.embed,
            view=self.view,
            delete_after=self.delete_after,
        )

    @classmethod
    def failure(cls, command: Command) -> Callable[[str], Response]:
        return lambda content: cls(
            content=content + "\n使い方：`" + command.usage + "`"
        )
