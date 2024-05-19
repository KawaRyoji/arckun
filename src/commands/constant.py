from typing import Literal

type commands = Literal["help", "commands", "boshu", "roll", "tenki", "youbou"]

command_explanation: dict[commands, dict[Literal["description", "usage"], str]] = {
    "help": {
        "description": "コマンドの概要と使い方を表示するよ。",
        "usage": "$help {調べたいコマンド}",
    },
    "commands": {
        "description": "使えるコマンドを表示するよ。",
        "usage": "$commands",
    },
    "boshu": {
        "description": "人を募集するよ。",
        "usage": "$boshu {募集したいゲーム} {集めたい人数}",
    },
    "roll": {
        "description": "サイコロを振るよ。",
        "usage": "$roll {サイコロの個数}d{サイコロの面数}",
    },
    "tenki": {
        "description": "都道府県の天気予報をだすよ。\n北海道は道南，道北，道東，道央に分かれてるよ。",
        "usage": "$tenki {都道府県}",
    },
    "youbou": {
        "description": "アークくんの改造案を提出するよ。",
        "usage": "$youbou",
    },
}

def format_command(name: commands) -> str:
    return "\n".join(
            [f"## {name}",
            f"{command_explanation.get(name).get("description")}",
            f"使い方：`{command_explanation.get(name).get("usage")}`"]
    )
