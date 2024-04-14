import random
from typing import override

from discord import Message

from ..utils import Failure, Result, Success
from .core import Command, response_using_text_message


class Roll(Command[str, str]):
    @override
    async def exec(self, *args: str) -> Result[str, str]:
        if len(args) == 0:
            return Failure("引数が足りないよ。")

        numbers = args[0].split("d")

        if len(numbers) < 2:
            return Failure("引数のフォーマットが違うよ。")

        try:
            dice = int(numbers[0])
            sides = int(numbers[1])

            if dice < 1 or dice > 100 or sides < 1 or sides > 100:
                return Success("回数と面数は1から99以下にしてね。")

            results = list(
                map(
                    lambda _: str(random.randint(1, sides)),
                    range(0, dice),
                )
            )

            return Success(", ".join(results))
        except ValueError:
            return Failure("個数と面数は整数で指定してね。")

    @override
    async def response(self, result: Result[str, str], message: Message) -> None:
        await response_using_text_message(result, message, self.usage)


roll = Roll("roll", "サイコロを振るよ。", "$roll {サイコロの個数}d{サイコロの面数}")
