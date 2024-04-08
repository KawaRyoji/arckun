import json
import traceback
from typing import Any

import discord

from .commands import commands
from .commands.command import Command, parse_message
from .utils import Failure, Result, Success, send_message

# presence, members, message_content以外のインテントを有効にする設定
intents = discord.Intents.default()
intents.message_content = True  # message_contentを有効化
COMMAND_PREFIX = "$"  # コマンドメッセージのプレフィックス

client = discord.Client(intents=intents)


async def _commands_func(*args: str) -> Result[str, str]:
    return Success(commands.show_all())


_commands = Command(
    "command", "すべてのコマンドを表示します。", "$commands", _commands_func
)


async def _help_func(*args: str) -> Result[str, str]:
    if len(args) == 0:
        return Failure("引数が足りないよ。")

    maybe_command = commands.search_from_name(args[0])

    if maybe_command is None:
        return Success("コマンド：" + args[0] + "は知らないよ。")
    else:
        return Success(str(maybe_command))


_help = Command(
    "help",
    "コマンドの概要と使い方を表示します。",
    "$help {調べたいコマンド}",
    _help_func,
)


@client.event
async def on_ready() -> None:
    print(f"login as name:{client.user}")


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:  # bot自身のメッセージには反応しない
        return

    try:
        name, args = parse_message(message)

        if not name.startswith(COMMAND_PREFIX):
            return

        name = name[1:]
        if name == "commands":
            maybe_command = _commands
        elif name == "help":
            maybe_command = _help
        else:
            maybe_command = commands.search_from_name(name)

        result = None if maybe_command is None else await maybe_command.exec(*args)

        match result:
            case Success():
                ret_message = result.value
            case Failure():
                ret_message = result.value + "\n使い方：`" + maybe_command.usage + "`"
            case _:
                return

        await send_message(message.channel, ret_message, mention_at=message.author)
    except Exception:
        await send_message(
            message.channel,
            "予期せぬエラーが発生しました。\n" + traceback.format_exc(),
            mention_at=message.author,
        )


with open("./env.json", "r") as f:
    token_file: dict[str, Any] = json.load(f)

client.run(token=token_file["TOKEN"])
