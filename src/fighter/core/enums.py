from enum import Enum, auto, IntEnum


class GameStateNum(Enum):
    START_MENU = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    INSTRUCTIONS = auto()


class FighterActionNUM(IntEnum):
    IDLE = 0
    RUN = 1
    JUMP = 2
    ATK1 = 3
    ATK2 = 4
    UNUSED = 5
    LIE = 6


class RecordField(Enum):
    TIMESTAMP = "timestamp"
    SCORE     = "score"
    LEVEL     = "level"
