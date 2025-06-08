from .base import GameState, IGame
import pygame, sys
from src.fighter.entities.player import Player
from ..core.enums import GameStateNum, RecordField
from ..core.constants import *
from src.fighter.entities.enemies.enemy_manager import EnemyManager
from src.fighter.assets.assets_path_enum import InGameImageKey
from src.graphics.scrolling_background import ScrollingBackground
from src.graphics.score_popup import ScorePopup

from logger import MyLogger
logger = MyLogger()


class Playing(GameState):
    def __init__(self, game: IGame):
        super().__init__(game)
        self.player = Player(self.assets, self.game)
        self.screen = self.game.screen

        self.bg_img_obj = self.game.assets.get_image(InGameImageKey.BACKGROUND)
        self.bg = ScrollingBackground(self.screen,
                                      self.bg_img_obj,
                                      self.game.WIDTH,
                                      SCROLL_SPEED
                                      )

        self.enemy_manager = EnemyManager(self.game)

        self.hud_font = pygame.font.Font(None, LEVEL_FONT_SIZE)   # 24-px default font
        self.hud_color = RED             # white text
        self.hud_margin = LEVEL_MARGIN_X
        self.popups = []
        self.score_font = pygame.font.Font(None, 32)

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

    def update(self):

        self.bg.update()
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update()

        self.enemy_manager.update_and_handle_kills(self.player, self.popups, self.hud_font)

        self.update_popups()

        state = self.check_player_collision()

        return state

    def update_popups(self):
        """Update all popups and remove expired ones"""
        # Update each popup
        for popup in self.popups:
            popup.update()

        # Remove expired popups
        self.popups = [popup for popup in self.popups if not popup.is_expired()]

    def check_player_collision(self):
        if self.player.attacking:
            return None  # i
        for e in self.enemy_manager.enemies:
            if e.alive and self.player.player_rect.colliderect(e.enemy_rect):
                return GameStateNum.GAME_OVER
        return None

    def draw(self, surf):
        self.bg.draw()
        self.player.draw()
        self.enemy_manager.draw(self.screen)
        self.update_score(surf)

        for popup in self.popups:
            popup.draw(surf)

        pygame.display.flip()

    def update_score(self, surf):
        score_surf = self.hud_font.render(f"{RecordField.SCORE.value}: {self.game.score}", True, self.hud_color)
        level_surf = self.hud_font.render(f"{RecordField.LEVEL.value}: {self.game.level}", True, self.hud_color)

        surf.blit(score_surf, (self.hud_margin, self.hud_margin))
        surf.blit(level_surf, (self.hud_margin, self.hud_margin + score_surf.get_height() + 2))


class GameOver(GameState):
    def __init__(self, game: IGame):
        super().__init__(game)
        self.font = pygame.font.SysFont(ARIAL, 48)
        self.small = pygame.font.SysFont(ARIAL, 24)
        self.header_font = pygame.font.SysFont(ARIAL, 32)
        self.screen = self.game.screen

        self._records_loaded = False
        self._top_records    = []

    def update(self):
        # once, when we first hit GameOver, save & load top records
        if not self._records_loaded:
            self.game.records.add(self.game.score, self.game.level)
            self.game.records.save()
            self._top_records = self.game.records.get_top(3)
            self._records_loaded = True
        return None

    def handle_events(self, events):
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    self.game.score = 0
                    self.game.level = 1
                    # reinitialize the game
                    self.game.states.pop(GameStateNum.PLAYING, None)
                    return GameStateNum.START_MENU
                elif ev.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    def draw(self, surf):
        # clear
        surf.fill((0, 0, 0))

        mid_x = self.game.WIDTH // 2
        mid_y = self.game.HEIGHT // 2

        # Game Over title
        title_surf = self.font.render("GAME OVER", True, WHITE)
        title_rect = title_surf.get_rect(center=(mid_x, mid_y - 100))
        surf.blit(title_surf, title_rect)

        # Prompt
        prompt = self.small.render("Press R to restart or Q to quit", True, WHITE)
        prompt_rect = prompt.get_rect(center=(mid_x, mid_y - 50))
        surf.blit(prompt, prompt_rect)

        # Show final score
        score_surf = self.small.render(f"Your Score: {self.game.score}", True, WHITE)
        score_rect = score_surf.get_rect(center=(mid_x, mid_y))
        surf.blit(score_surf, score_rect)

        # High Scores header
        hs_header = self.header_font.render("High Score Records:", True, RED)
        hs_x = 40
        hs_y = mid_y + 80
        surf.blit(hs_header, (hs_x, hs_y))

        for i, entry in enumerate(self._top_records):
            line = f"{entry['score']:>3} points       level {entry['level']}                           in date: {entry['timestamp'][:19]}"
            line_surf = self.small.render(line, True, WHITE)
            line_rect = line_surf.get_rect(center=(mid_x + 100, mid_y + 50 * (i+2)))
            surf.blit(line_surf, line_rect)

        pygame.display.flip()


class Instructions(GameState):
    def __init__(self, game: IGame):
        super().__init__(game)

        self.instruction_image = self.game.assets.get_image(InGameImageKey.INSTRUCTION)
        # prepare text
        self.font = pygame.font.Font(None, INST_FONT_SIZE)
        self.lines = INSTRUCTION_LINES

    def draw(self, surf):
        inst_screen = self.game.screen

        width, height = self.game.WIDTH, self.game.HEIGHT

        scaled_image = pygame.transform.scale(
            self.instruction_image,
            (width, height)
        )

        inst_screen.blit(scaled_image, CENTER)

        # render all text surfaces first
        rendered = []
        for idx, line in enumerate(self.lines):
            color = RED if idx == 0 else WHITE
            surf = self.font.render(line, True, color)
            rendered.append(surf)

        # center the title (idx 0) at top of screen
        title_surf = rendered[0]
        title_rect = title_surf.get_rect(centerx=width // 2, y=INST_MARGIN_Y)
        inst_screen.blit(title_surf, title_rect)

        # stack the rest under the title
        y = title_rect.bottom + INST_LINE_SPACING
        for surf in rendered[1:]:
            rect = surf.get_rect(x=INST_MARGIN_X, y=y)
            inst_screen.blit(surf, rect)
            y += INST_LINE_SPACING

        pygame.display.update()

    def handle_events(self, events):
        #any Click to exit the function
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return GameStateNum.START_MENU

    def update(self):
        return None


class StartMenu(GameState):
    def __init__(self, game: IGame):
        super().__init__(game)
        self.font = pygame.font.Font(None, MM_FONT_SIZE)
        self.title_text = self.font.render(MM_TITLE, True, RED)
        self.option_rects = []

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(mouse_pos):
                        if i == 0:  # Start Game
                            return GameStateNum.PLAYING
                        elif i == 1:  # Instructions
                            return GameStateNum.INSTRUCTIONS
                        elif i == 2:  # Quit
                            pygame.quit()
        return None

    def draw(self, surf):
        bg_menu = self.assets.get_image(InGameImageKey.BG_MENU)
        surf.blit(bg_menu, CENTER)
        screen_width = self.game.WIDTH

        # draw title by (screen_width/2 - title_width/2) because we want it in the center title_width/2 makes sure it is centered
        surf.blit(self.title_text, (screen_width // 2 - self.title_text.get_width() // 2, MM_Y_OFFSET))

        self.option_rects = []
        for i, option in enumerate(MM_OPTIONS):
            option_text = self.font.render(option, True, WHITE)

            # Positions texts in center horizontally and each line is spaced 60 (Distance) pixels apart, starting from y = 150 (Offset)
            rect = option_text.get_rect(center=(screen_width // 2, MM_OPTIONS_Y_OFFSET + i * MM_OPTIONS_DISTANCE))
            self.option_rects.append(rect)
            surf.blit(option_text, rect)

    def update(self):
        return None
