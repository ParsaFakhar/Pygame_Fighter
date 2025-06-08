import pygame
from src.fighter.states.base import IGame
from src.fighter.assets.assets_path_enum import InGameImageKey, SoundKey
from src.fighter.assets.asset_manager import AssetManager
from src.fighter.assets.audio_manager import AudioManager
from src.fighter.core.constants import CAPTION, FRAMES, DEFAULT_RECORD_PATH
from src.fighter.core.enums import GameStateNum
from src.fighter.metaclass import SingletonABCMeta
from src.fighter.states.states import StartMenu, Playing, GameOver, Instructions
from src.fighter.assets.record_manager import RecordManager
from logger import MyLogger

logger = MyLogger()


class Game(IGame, metaclass=SingletonABCMeta):
    def __init__(self):
        pygame.init()
        self.assets = AssetManager()
        self.audio = AudioManager(self.assets)
        self.records = RecordManager(DEFAULT_RECORD_PATH)
        self.states = {}

        self.score = 0
        self.level = 1

        self.bg = InGameImageKey.BACKGROUND

        # Load background first to get its size
        self.WIDTH, self.HEIGHT = self.assets.get_width_height(self.bg)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.assets.get_image(self.bg)

        self.running = True

        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()

        self.audio.play_music(SoundKey.BG_MUSIC, loops=-1)

        self.current_state = self.get_state(GameStateNum.START_MENU)

    def get_state(self, state_enum):
        if state_enum not in self.states:
            if state_enum == GameStateNum.START_MENU:
                self.states[state_enum] = StartMenu(self)
            elif state_enum == GameStateNum.PLAYING:
                self.states[state_enum] = Playing(self)
            elif state_enum == GameStateNum.GAME_OVER:
                self.states[state_enum] = GameOver(self)
            elif state_enum == GameStateNum.INSTRUCTIONS:
                self.states[state_enum] = Instructions(self)
        return self.states[state_enum]

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            # Handle state-specific events

            result = self.current_state.handle_events(events)
            if result:
                self.current_state = self.get_state(result)

            # Update current state
            result = self.current_state.update()
            if result:
                self.current_state = self.get_state(result)

            self.current_state.draw(self.screen)

            # Draw current state

            pygame.display.flip()
            self.clock.tick(FRAMES)

    def stop(self):
        pass

#  test 22
if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        game.stop()
