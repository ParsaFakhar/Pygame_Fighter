import pygame
from src.fighter.assets.assets_path_enum import SoundKey  # wherever your SoundKey lives
from .asset_manager import AssetManager


class AudioManager:
    def __init__(self, assets: AssetManager):
        pygame.mixer.init()
        self._assets = assets

    @staticmethod
    def play_music(key: SoundKey, loops: int = -1, start: float = 0.0):
        pygame.mixer.music.load(str(key.path))
        pygame.mixer.music.play(loops, start)

    @staticmethod
    def stop_music():
        pygame.mixer.music.stop()

    def play_sfx(self, key: SoundKey):
        """Play a one‐off sound effect."""
        sfx = self._assets.get_sound(key)
        sfx.play()
