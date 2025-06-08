from abc import ABC, abstractmethod
from src.fighter.core.constants import ENEMY_DEFAULT_SCORE


class Enemy(ABC):
    score_value = ENEMY_DEFAULT_SCORE

    def __init__(self, x, y, velocity, game):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.alive = True
        self.assets = game.assets
        self.game = game

    @abstractmethod
    def update(self):
        """Advance position, animation, and rect."""
        pass

    @abstractmethod
    def draw(self, win):
        """Blit current frame to win."""
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        return self.alive

    @property
    def enemy_rect(self):
        return



