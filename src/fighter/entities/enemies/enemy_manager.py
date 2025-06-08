import random
from . import ENEMY_REGISTRY
from src.fighter.core.constants import *
from src.fighter.core.enums import GameStateNum
from src.fighter.assets.assets_path_enum import SoundKey
from src.graphics.score_popup import ScorePopup
import pygame
from logger import MyLogger

logger = MyLogger()


class EnemyManager:
    def __init__(self, game):
        self.game = game
        self.assets = game.assets
        self.ground = GROUND
        self.killed_count = 0
        self.enemies = []

        logger.info(f"EnemyManager initialized for level {self.game.level}")
        self.enemies = self.create_random_enemies(level=self.game.level)

    def update_and_handle_kills(self, player, popup_list, popup_font):
        """
        1) Move enemies, detect kills
        2) For each kill: spawn a ScorePopup, play sound, increment score
        3) Cull dead enemies
        4) Return nothing (all side-effects internalized)
        """
        # Spawn wave if needed
        if not self.enemies:
            self.enemies = self.create_random_enemies(self.game.level)

        # Move & detect kill events
        for e in self.enemies:
            if e.alive:
                e.update()
                if player.attacking and player.check_collision_with_enemy(e.enemy_rect):
                    e.alive = False

                    self.play_kill_sfx()

                    # spawn score popup
                    popup_list.append(ScorePopup(f"+{e.score_value}", (e.enemy_rect.centerx, e.enemy_rect.top), popup_font))

                    self.game.score += e.score_value
                    self.killed_count += 1

        # Remove dead enemies
        self.enemies = [e for e in self.enemies if e.alive]

        # Level up
        if self.killed_count >= REQUIRED_KILL_LEVEL:
            self.game.level += 1
            self.killed_count = 0

    def play_kill_sfx(self):
        """
        Look for free channel to play sound
        :return:
        """
        ch = pygame.mixer.find_channel()
        if ch:
            self.game.audio.play_sfx(SoundKey.COIN)
        else:
            pygame.mixer.Channel(0).play(self.game.assets.get_sound(SoundKey.COIN))

    def draw(self, win):
        logger.debug(f"Drawing {len(self.enemies)} enemies")
        for enemy in self.enemies:
            if enemy.is_alive():  # Only draw alive enemies
                enemy.draw(win)

    def create_random_enemies(self, level: int):
        enemies = []
        enemy_count = min(2 + level, 8)

        logger.info(f"Creating {enemy_count} enemies for level {level}")
        logger.debug(f"registry is: {ENEMY_REGISTRY} before entering enemy creation loop")

        for _ in range(enemy_count):
            enemy_x = random.randint(self.game.WIDTH + ENEMY_OFFSET_RANDOM, self.game.WIDTH + ENEMY_OFFSCREEN)
            enemy_y = self.ground

            velocity = random.randint(ENEMY_BASE_VELOCITY, min(ENEMY_MINIMUM_VELOCITY + level, ENEMY_MAXIMUM_VELOCITY))
            enemy_class = random.choice(ENEMY_REGISTRY)

            logger.debug(f"Created {enemy_class.__name__} at ({enemy_x}, {enemy_y}) with velocity {velocity}")

            enemies.append(enemy_class(enemy_x,
                                       enemy_y,
                                       velocity,
                                       self.game)
                           )
            logger.info(f"Enemy {enemy_class.__name__} created")
            logger.info(f"Successfully created {len(enemies)} enemies")
        return enemies
