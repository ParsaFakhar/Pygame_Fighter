import pygame
from . import register_enemy, ENEMY_REGISTRY
from .enemy_base import Enemy
from ...core.constants import *
from src.fighter.assets.assets_path_enum import EntityImageKey, SoundKey

from logger import MyLogger

logger = MyLogger()


@register_enemy
class Wizard(Enemy):
    def __init__(self, x, y, velocity, game):
        super().__init__(x, y, velocity, game)

        # Run
        self.current_action = 1

        self.animations = self.assets.get_animation(EntityImageKey.WIZARD,
                                                    WIZARD_SIZE,
                                                    WIZARD_SCALE,
                                                    WIZARD_PER_ACTION
                                                    )
        self.x = WIZARD_X
        self.y = WIZARD_Y

        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

        self.current_animation = self.animations[self.current_action]

        self.rect = pygame.Rect(self.x, self.y, WIZARD_RECT_W, WIZARD_RECT_H)
        self.game.audio.play_sfx(SoundKey.EVIL)

        logger.info(f"Wizard created at ({x}, {y}) with velocity {velocity}")

    def is_alive(self):
        return self.alive

    def draw(self, win):
        surf = self.current_animation[self.current_frame]
        frame = pygame.transform.flip(surf, True, False)

        win.blit(frame, (self.x - WIZARD_OFFSET[0], self.y - WIZARD_OFFSET[1]))

        if DEBUG:
            pygame.draw.rect(win, (255, 0, 0), self.rect, 1)

    def update(self):
        # move left
        self.x -= self.velocity
        # animate
        now = pygame.time.get_ticks()
        if now - self.last_update > FRAME_DURATION:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_action])

        self._update_rect()

        if self.x + self.rect.width < 0:
            self.alive = False

            logger.debug(f"Wizard marked dead - off screen at x: {self.x}")

    def _update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, WIZARD_RECT_W, WIZARD_RECT_H)

    @property
    def enemy_rect(self):
        return self.rect
