from typing import override

import discord

from .constant import command_explanation, format_command
from .core import Command, Response


class Help(Command):
    @override
    def exec(self, source_message: discord.Message, *args: str) -> Response:
        if len(args) == 0:
            return Response.failure(self)("引数が足りないよ。")

        maybe_command = command_explanation.get(args[0])

        if maybe_command is None:
            return Response("コマンド：" + args[0] + "は知らないよ。")
        else:
            return Response(format_command(args[0]))
