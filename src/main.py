import json
from typing import Any

import discord

from .commands.core import parse_message
from .commands.factory import create_command

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

    try:
        maybe_content = parse_message(message)

        if maybe_content is None:
            return

        name, args = maybe_content
        command = create_command(name)

        if command is None:
            return

        response = command.exec(message, *args)
        await response.send(message)

    except Exception as e:
        await message.reply("予期せぬエラーが発生しました。\n" + str(e))


with open("./env.json", "r") as f:
    token_file: dict[str, Any] = json.load(f)

client.run(token=token_file["TOKEN"])
