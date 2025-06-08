from dataclasses import dataclass


@dataclass(slots=True)
class ScrollingBackground:
    screen:       any
    image:        any
    bg_width:     int
    scroll_speed: int
    x2:           int
    x1:           int = 0

    def __init__(self, screen, image, bg_width, scroll_speed):
        self.image = image
        self.scroll_speed = scroll_speed
        self.bg_width = bg_width
        self.screen = screen
        self.x1 = 0
        self.x2 = bg_width

    def update(self):
        self.x1 -= self.scroll_speed
        self.x2 -= self.scroll_speed

        if self.x1 <= -self.bg_width:
            self.x1 = self.bg_width

        if self.x2 <= -self.bg_width:
            self.x2 = self.bg_width

    def draw(self):
        self.screen.blit(self.image, (self.x1, 0))
        self.screen.blit(self.image, (self.x2, 0))

