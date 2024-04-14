from typing import override

import discord

from ...utils import Failure, Result, Success
from .. import commands
from ..core import Command, response_using_text_message


class Help(Command[str, str]):
    @override
    async def exec(self, *args: str) -> Result[str, str]:
        if len(args) == 0:
            return Failure("引数が足りないよ。")

        maybe_command = commands.search_from_name(args[0])

        if maybe_command is None:
            return Success("コマンド：" + args[0] + "は知らないよ。")
        else:
            return Success(str(maybe_command))

    @override
    async def response(
        self, result: Result[str, str], message: discord.Message
    ) -> None:
        await response_using_text_message(result, message, self.usage)


help = Help("help", "コマンドの概要と使い方を表示します。", "$help {調べたいコマンド}")
