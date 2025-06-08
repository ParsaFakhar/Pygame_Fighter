from abc import ABC, abstractmethod, ABCMeta


class IGame(ABC):
    @abstractmethod
    def get_state(self, state_enum):
        pass

    @abstractmethod
    def run(self):
        pass


class GameState(ABC):
    def __init__(self, game):
        self.game = game
        self.assets = game.assets

    @abstractmethod
    def handle_events(self, events):
        """Process pygame events."""
        pass

    @abstractmethod
    def update(self):
        """Advance game logic by dt seconds."""
        pass

    @abstractmethod
    def draw(self, surf):
        """Render this state to the given surface."""
        pass
