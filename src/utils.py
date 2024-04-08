from dataclasses import dataclass

import discord


async def send_message(
    channel: discord.TextChannel | discord.GroupChannel | discord.VoiceChannel,
    content: str,
    mention_at: discord.User | discord.Member | None,
) -> None:
    builded_content = "" if mention_at is None else mention_at.mention + " " + content
    await channel.send(builded_content)


@dataclass(frozen=True)
class Success[T]:
    value: T


@dataclass(frozen=True)
class Failure[E]:
    value: E


type Result[T, E] = Success[T] | Failure[E]
