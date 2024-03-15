# Common Imports
from enum import Enum, unique


@unique
class Action(Enum):
    Buy = 1
    Sell = 2
