from .boshu import boshu
from .core import Commands
from .roll import roll
from .tenki import tenki

# ここに使えるすべてのコマンドを記述
commands = Commands([roll, tenki, boshu])
