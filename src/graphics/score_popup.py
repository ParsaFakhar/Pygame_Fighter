# src/fighter/ui/score_popup.py

import pygame
import time


class ScorePopup:
    def __init__(self, text: str, pos: tuple[int,int], font: pygame.font.Font, color=(255,255,0), lifetime=0.8):
        self.text      = text
        self.font      = font
        self.color     = color
        self.pos       = pygame.math.Vector2(pos)
        self.spawn_t   = time.time()
        self.lifetime  = lifetime
        self.surf      = font.render(text, True, color)
        self.alpha     = 255

    def update(self):
        """Returns False once expired."""
        elapsed = time.time() - self.spawn_t
        if elapsed > self.lifetime:
            return False
        # float up a little
        self.pos.y -= 30 * (1/60)   # 30 px/sec upward
        # fade out in last 20% of lifetime
        if elapsed > self.lifetime * 0.8:
            frac = (elapsed - self.lifetime*0.8) / (self.lifetime*0.2)
            self.alpha = max(0, int(255*(1 - frac)))
            self.surf.set_alpha(self.alpha)
        return True

    def draw(self, surf):
        surf.blit(self.surf, self.pos)

    def is_expired(self):
        return self.lifetime <= 0

