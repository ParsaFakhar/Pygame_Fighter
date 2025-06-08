# assets/asset_manager.py
import pygame
from ..metaclass import SingletonMeta
from src.fighter.assets.assets_path_enum import *
from typing import Union
from src.fighter.assets.sprite_loader import load_frames
from logger import MyLogger

logger = MyLogger()

ImageKey = Union[InGameImageKey, EntityImageKey]


class AssetManager(metaclass=SingletonMeta):
    def __init__(self):
        self._images = {}
        self._sounds = {}
        self._fonts = {}
        self._animations = {}

    def get_image(self, key: ImageKey) -> pygame.Surface:
        if key not in self._images:
            img = pygame.image.load(str(key.path)).convert_alpha()
            self._images[key] = img
        return self._images[key]

    @staticmethod
    def get_width_height(key: ImageKey) -> tuple[int,int]:
        # Load raw (no conversion) just to get dimensions
        raw = pygame.image.load(str(key.path))
        return raw.get_size()

    def get_sound(self, key: SoundKey) -> pygame.mixer.Sound:
        if key not in self._sounds:
            self._sounds[key] = pygame.mixer.Sound(str(key.path))
        return self._sounds[key]

    def get_font(self, key: FontKey) -> pygame.font.Font:
        if key not in self._fonts:
            # FontKey.path and FontKey.size
            self._fonts[key] = pygame.font.Font(str(key.path), key.size)
        return self._fonts[key]

    def get_animation(self, key, size, scale, frames_per):
        if key not in self._animations:
            sheet = self.get_image(key)
            self._animations[key] = load_frames(sheet, size, scale, frames_per)
        return self._animations[key]

    def clear_cache(self):
        self._images.clear()
        self._sounds.clear()
        self._fonts.clear()
        self._animations.clear()
