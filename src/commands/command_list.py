from typing import override

import discord

from ..commands.core import Command, Response
from .constant import command_explanation, format_command


class CommandList(Command):
    @override
    def exec(self, source_message: discord.Message, *args: str) -> Response:
        content = "\n".join(list(map(format_command, command_explanation.keys())))
        return Response(content)
