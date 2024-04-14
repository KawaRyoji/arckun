from typing import override

from discord import Message

from ...commands.core import Command, response_using_text_message
from ...utils import Result, Success
from .. import commands


class CommandList(Command[str, str]):
    @override
    async def exec(self, *args: str) -> Result[str, str]:
        return Success(commands.show_all())

    @override
    async def response(self, result: Result[str, str], message: Message) -> None:
        await response_using_text_message(result, message, self.usage)


command_list = CommandList("commands", "使えるコマンドを表示するよ", "$commands")
