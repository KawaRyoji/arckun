from typing import override

import discord

from .core import Command, Response


class _YoubouView(discord.ui.View):
    @discord.ui.button(label="submit", style=discord.ButtonStyle.success)
    async def submit(
        self, interaction: discord.Interaction, button: discord.Button
    ) -> None:
        pass


class _YoubouModal(discord.ui.Modal, title="アークくん改造要望"):
    proposal = discord.ui.TextInput(
        label="アークくんの改造案を書いてね",
        placeholder="10～300字以内",
        style=discord.TextStyle.long,
        required=True,
        min_length=10,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            "書いてくれてありがとう！", ephemeral=True
        )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        await interaction.response.send_message(
            "予期せぬエラーが発生しました。" + str(error), ephemeral=True
        )


class Youbou(Command):
    @override
    def exec(self, source_message: discord.Message, *args: str) -> Response:
        pass
