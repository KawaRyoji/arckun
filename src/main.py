import json
from typing import Any

import discord

from .commands import commands
from .commands.core import COMMAND_PREFIX, parse_message
from .commands.special import command_list, help

# presence, members, message_content以外のインテントを有効にする設定
intents = discord.Intents.default()
intents.message_content = True  # message_contentを有効化

client = discord.Client(intents=intents)


@client.event
async def on_ready() -> None:
    print(f"login as name:{client.user}")


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:  # bot自身のメッセージには反応しない
        return

    print("received: " + message.content)

    try:
        name, args = parse_message(message)

        if not name.startswith(COMMAND_PREFIX):
            return

        name = name[1:]
        if name == "commands":
            command = command_list
        elif name == "help":
            command = help
        else:
            maybe_command = commands.search_from_name(name)
            if maybe_command is None:
                return
            command = maybe_command

        result = None if command is None else await command.exec(*args)
        await command.response(result, message)

    except Exception as e:
        message.reply("予期せぬエラーが発生しました。\n" + str(e))


with open("./env.json", "r") as f:
    token_file: dict[str, Any] = json.load(f)

client.run(token=token_file["TOKEN"])
