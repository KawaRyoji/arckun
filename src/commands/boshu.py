from dataclasses import dataclass
from typing import Callable, Optional, override

import discord

from ..utils import Failure, Result, Success, use_state
from .core import Command, on_failure_with_usage


@dataclass(frozen=True)
class _BoshuModel:
    title: str
    remain: int
    users: list[discord.User]

    def add_user(self, user: discord.User) -> "_BoshuModel":
        if user in self.users:
            return self
        else:
            return self.copy_with(remain=self.remain - 1, users=self.users + [user])

    def del_user(self, user: discord.User) -> "_BoshuModel":
        if user in self.users:
            return self.copy_with(
                remain=self.remain + 1,
                users=list(filter(lambda u: u != user, self.users)),
            )
        else:
            return self

    def copy_with(
        self,
        title: Optional[str] = None,
        remain: Optional[int] = None,
        users: Optional[list[discord.User]] = None,
    ) -> "_BoshuModel":
        return _BoshuModel(
            self.title if title is None else title,
            self.remain if remain is None else remain,
            self.users if users is None else users,
        )

    def to_message_text(self) -> None:
        return "\n".join(
            [
                "# " + self.title + f"@{self.remain}",
                "## 参加する人",
                *self.users_to_strings(),
            ],
        )

    def users_to_strings(self) -> list[str]:
        return list(map(lambda user: "- " + user.display_name, self.users))


class _BoshuView(discord.ui.View):
    def __init__(
        self,
        state: Callable[[], _BoshuModel],
        set_state: Callable[[_BoshuModel], None],
        *,
        timeout: float | None = 180,
    ) -> None:
        super().__init__(timeout=timeout)
        self.state = state
        self.set_state = set_state

    @discord.ui.button(label="join", style=discord.ButtonStyle.success)
    async def join(
        self, interaction: discord.Interaction, button: discord.Button
    ) -> None:
        self.set_state(self.state().add_user(interaction.user))
        await interaction.response.defer()  # コマンドが成功するおまじない

        if self.state().remain <= 0:
            await interaction.edit_original_response(
                content="\n".join(
                    ["# " + self.state().title + "〆", *self.state().users_to_strings()]
                )
            )
        await interaction.edit_original_response(content=self.state().to_message_text())

    @discord.ui.button(label="quit", style=discord.ButtonStyle.secondary)
    async def quit(
        self, interaction: discord.Interaction, button: discord.Button
    ) -> None:
        self.set_state(self.state().del_user(interaction.user))
        await interaction.response.defer()  # コマンドが成功するおまじない
        await interaction.edit_original_response(content=self.state().to_message_text())


class Boshu(Command[_BoshuModel, str]):
    @override
    async def exec(self, *args: str) -> Result[_BoshuModel, str]:
        if len(args) < 2:
            return Failure("引数が足りないよ。")

        title = args[0]
        try:
            remain = int(args[1])
            if remain < 1 or remain > 20:
                raise ValueError()
        except ValueError:
            return Failure("募集人数は1～20にしてね。")

        return Success(_BoshuModel(title, remain, []))

    @override
    async def response(
        self, result: Result[_BoshuModel, str], message: discord.Message
    ) -> None:
        match result:
            case Success():
                state, set_state = use_state(
                    result.value.copy_with(users=[message.author])
                )
                await message.reply(
                    content=state().to_message_text(),
                    view=_BoshuView(state, set_state, timeout=5000),
                )
            case Failure():
                await on_failure_with_usage(result, message, self.usage)


boshu = Boshu("boshu", "人を募集するよ。", "$boshu {募集したいゲーム} {集めたい人数}")
