# src/fighter/entities/enemies/__init__.py
ENEMY_REGISTRY = []


def register_enemy(cls):
    ENEMY_REGISTRY.append(cls)
    return cls


# import these modules so their @register_enemy decorators run
from .pig import Pig
from .wizard import Wizard

