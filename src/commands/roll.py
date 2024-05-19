import random
from typing import override

import discord

from .core import Command, Response


class Roll(Command):
    @override
    def exec(self, source_message: discord.Message, *args: str) -> Response:
        failure = Response.failure(self)

        if len(args) == 0:
            return failure("引数が足りないよ。")

        numbers = args[0].split("d")

        if len(numbers) < 2:
            return failure("引数のフォーマットが違うよ。")

        try:
            dice = int(numbers[0])
            sides = int(numbers[1])

            if dice < 1 or dice > 100 or sides < 1 or sides > 100:
                return Response("回数と面数は1から99以下にしてね。")

            results = list(
                map(
                    lambda _: str(random.randint(1, sides)),
                    range(0, dice),
                )
            )

            return Response(", ".join(results))
        except ValueError:
            return failure("個数と面数は整数で指定してね。")
