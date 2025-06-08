from enum import Enum
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
IMG_DIR = BASE_DIR / "assets" / "images"
AUDIO_DIR = BASE_DIR / "assets" / "audio"
# FONT_DIR = BASE_DIR / "assets" / "fonts"


class AssetEnumMixin:
    def __init__(self, path: Path, desc: str):
        self.path = path
        self.desc = desc


class InGameImageKey(AssetEnumMixin, Enum):
    BACKGROUND = (
        IMG_DIR / "background.jpg",
        "Mountain-at-dusk panorama used in main gameplay.",
    )
    GAME_OVER = (
        IMG_DIR / "gameOverImage.jpg",
        "Full-screen 'Game Over' background.",
    )
    INSTRUCTION = (
        IMG_DIR / "InstructionImage.jpg",
        "Instruction screen background with controls.",
    )
    BG_MENU = (
        IMG_DIR / "bg_menu.jpg",
        "Main menu background image.",
    )


class EntityImageKey(AssetEnumMixin, Enum):
    PLAYER_SPRITE = (
        IMG_DIR / "warrior.png",
        "Warrior sprite sheet for player animations.",
    )
    WIZARD = (
        IMG_DIR / "enemies" / "wizard.png",
        "Wizard enemy sprite sheet.",
    )
    PIG = (
        IMG_DIR / "enemies" / "pig.png",
        "Pig enemy static sprite.",
    )


class SoundKey(AssetEnumMixin, Enum):
    BG_MUSIC = (
        AUDIO_DIR / "champion.mp3",
        "Background music track."
    )
    SWORD = (
        AUDIO_DIR / "sword.wav",
        "Sword swing sound effect."
    )
    EVIL = (
        AUDIO_DIR / "evil.mp3",
        "Evil laugh/jingle sound effect."
    )
    COIN = (
        AUDIO_DIR / "coin.wav",
        "Pick Up Scores By Killing Enemies sound effect."
    )


class FontKey(AssetEnumMixin, Enum):
    pass


