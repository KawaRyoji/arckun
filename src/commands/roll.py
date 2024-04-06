import random

import discord

from ..utils import send_message
from .command import Command, parse_message


async def _roll(message: discord.Message) -> None:
    _, args = parse_message(message)

    if len(args) == 0:
        await send_message(
            message.channel,
            "引数が足りないよ。`$dice {サイコロの個数}d{サイコロの面数}`で指定してね。",
            mention_at=message.author,
        )
        return

    numbers = args[0].split("d")

    if len(numbers) < 2:
        await send_message(
            message.channel,
            "引数のフォーマットが違うよ。`$dice {サイコロの個数}d{サイコロの面数}`で指定してね。",
            mention_at=message.author,
        )
        return

    try:
        num_of_dice = int(numbers[0])
        num_of_sides = int(numbers[1])
        results = list(
            map(lambda _: str(random.randint(1, num_of_sides)), range(0, num_of_dice))
        )
        await send_message(
            message.channel,
            ", ".join(results),
            mention_at=message.author,
        )
    except ValueError:
        await send_message(
            message.channel,
            "個数と面数は数字で指定してね。`$dice {サイコロの個数}d{サイコロの面数}`で指定してね。",
            mention_at=message.author,
        )


roll = Command(
    "roll", "サイコロを振ります。", "`$dice {サイコロの個数}d{サイコロの面数}`", _roll
)
