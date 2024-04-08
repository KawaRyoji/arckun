import random

from ..utils import Failure, Result, Success
from .command import Command


async def _roll(*args: str) -> Result[str, str]:
    if len(args) == 0:
        return Failure("引数が足りないよ。")

    numbers = args[0].split("d")

    if len(numbers) < 2:
        return Failure("引数のフォーマットが違うよ。")

    try:
        num_of_dice = int(numbers[0])
        num_of_sides = int(numbers[1])
        results = list(
            map(lambda _: str(random.randint(1, num_of_sides)), range(0, num_of_dice))
        )

        return Success(", ".join(results))
    except ValueError:
        return Failure("個数と面数は整数で指定してね。")


roll = Command(
    "roll", "サイコロを振ります。", "$roll {サイコロの個数}d{サイコロの面数}", _roll
)
