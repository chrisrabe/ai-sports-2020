from . import random_strategy
from . import flee_strategy
from . import move_strategy
from . import basic_bomb_strategy
from . import reload_strategy
from . import treasure_strategy
from . import ore_bomb_strategy
from . import utils
from . import bomb_placement_strategy
from . import kill_strategy
from . import retreat_strategy
from . import smart_bomb_strategy


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


def BombPlacementStrategy():
    return bomb_placement_strategy.BombPlacementStrategy()


def TreasureStrategy():
    return treasure_strategy.TreasureStrategy()


def OreBombStrategy():
    return ore_bomb_strategy.OreBombStrategy()


def KillStrategy():
    return kill_strategy.KillStrategy()


def RetreatStrategy():
    return retreat_strategy.RetreatStrategy()


def SmartBombStrategy():
    return smart_bomb_strategy.SmartBombStrategy()
