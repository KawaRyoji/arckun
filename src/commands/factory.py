from .boshu import Boshu
from .command_list import CommandList
from .constant import command_explanation
from .core import Command
from .help import Help
from .roll import Roll
from .tenki import Tenki
from .youbou import Youbou


def create_command(name: str) -> Command | None:
    explanation = command_explanation.get(name)
    if explanation is None:
        return None

    description = explanation.get("description")
    usage = explanation.get("usage")

    match name:
        case "help":
            return Help("help", description, usage)
        case "commands":
            return CommandList("commands", description, usage)
        case "boshu":
            return Boshu("boshu", description, usage)
        case "roll":
            return Roll("roll", description, usage)
        case "tenki":
            return Tenki("tenki", description, usage)
        case "youbou":
            return Youbou("youbou", description, usage)
        case _:
            return None
