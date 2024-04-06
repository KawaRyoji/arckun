import json
from typing import Any

import discord

from utils import send_message

from .commands import commands

# presence, members, message_content以外のインテントを有効にする設定
intents = discord.Intents.default()
intents.message_content = True  # message_contentを有効化

client = discord.Client(intents=intents)


@client.event
async def on_ready() -> None:
    print(f"login as name:{client.user}")


@client.event
async def on_message(message: discord.Message) -> None:
    try:
        if message.author == client.user:  # bot自身のメッセージには反応しない
            return

        maybe_command = commands.search_from_message(message)

        if not maybe_command is None:
            await maybe_command.exec(message)

    except Exception as e:
        await send_message(
            message.channel,
            "予期せぬエラーが発生しました。Oops!\n" + str(e.with_traceback()),
            mention_at=message.author,
        )


with open("./env.json", "r") as f:
    token_file: dict[str, Any] = json.load(f)

client.run(token=token_file["TOKEN"])
