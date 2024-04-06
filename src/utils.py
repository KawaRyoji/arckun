import discord


async def send_message(
    channel: discord.TextChannel | discord.GroupChannel | discord.VoiceChannel,
    content: str,
    mention_at: discord.User | discord.Member | None,
) -> None:
    builded_content = "" if mention_at is None else mention_at.mention + " " + content
    await channel.send(builded_content)
