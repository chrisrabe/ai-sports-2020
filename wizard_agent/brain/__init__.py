from . import random_strategy
from . import flee_strategy
from . import move_strategy
from . import basic_bomb_strategy
from . import reload_strategy
from . import treasure_strategy
from . import utils


def RandomStrategy():
    return random_strategy.RandomStrategy()

def FleeStrategy():
    return flee_strategy.FleeStrategy()

def MoveStrategy():
    return move_strategy.MoveStrategy()

def BasicBombStrategy():
    return basic_bomb_strategy.BasicBombStrategy()

def ReloadStrategy():
    return reload_strategy.ReloadStrategy()

def TreasureStrategy():
    return treasure_strategy.TreasureStrategy()