from . import register_enemy
from .enemy_base import Enemy
from src.fighter.assets.assets_path_enum import EntityImageKey
import pygame
from src.fighter.core.constants import *
from logger import MyLogger

logger = MyLogger()


@register_enemy
class Pig(Enemy):
    score_value = PIG_SCORE

    def __init__(self, x, y, velocity, game):
        super().__init__(x, y, velocity, game)
        # pig only has a single image
        self.image = self.game.assets.get_image(EntityImageKey.PIG)
        self.image = pygame.transform.scale(self.image, PIG_SIZE)
        # Update coordinates to match rect
        self.x = PIG_X
        self.y = PIG_Y

        # initialize piggy rect
        self.rect = pygame.Rect(self.x, self.y, PIG_SIZE[0], PIG_SIZE[1])

    def update(self):
        # move left
        self.x -= self.velocity

        # update rect's position using middle of the bottom side of the rectangle
        self.rect.midbottom = (self.x, self.y)

        self._update_rect()

        # if off-screen, mark dead
        if self.x + self.rect.width < 0:
            self.alive = False
            logger.debug(f"Pig marked dead - off screen at x: {self.x}")

    def draw(self, win):
        # adjust the pig's rect position to match the image
        win.blit(self.image, (self.x - PIG_OFFSET[0], self.y - PIG_OFFSET[1]))
        if DEBUG:
            pygame.draw.rect(win, (255, 0, 0), self.rect, 1)

    def is_alive(self):
        return self.alive

    def _update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, PIG_RECT_W, PIG_RECT_H)

    @property
    def enemy_rect(self):
        """Get current collision rect"""
        return self.rect
