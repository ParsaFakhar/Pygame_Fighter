import pygame
from ..core.constants import *
from ..core.enums import FighterActionNUM
from src.fighter.assets.assets_path_enum import *
from src.fighter.states.states import *

from logger import MyLogger

logger = MyLogger()


class Player:
    def __init__(self, assets, game):
        self.game = game
        self.assets = assets
        self._initialize_state()
        self._load_animations()
        self._setup_physics()

    def _initialize_state(self):
        self.player_position = pygame.math.Vector2(PLAYER_X, PLAYER_Y)
        self.rect_size = pygame.math.Vector2(PLAYER_RECT_W, PLAYER_RECT_H)
        self.facing_right = True
        self.velocity = pygame.math.Vector2(0, 0)
        self.alive = True
        self.rect = pygame.Rect(self.player_position.x,
                                self.player_position.y,
                                self.rect_size.x,
                                self.rect_size.y
                                )
        self.jumping = False
        self.attacking = None
        self.facing_right = True

        self.bg_width = self.game.WIDTH
        self.bg_height = self.game.HEIGHT

    def _load_animations(self):
        """Load all animation frames from asset manager"""
        self.animations = self.assets.get_animation(EntityImageKey.PLAYER_SPRITE,
                                                    PLAYER_SIZE,
                                                    PLAYER_SCALE,
                                                    PLAYER_PER_ACTION
                                                    )

        self.current_action = FighterActionNUM.IDLE
        self.current_frame = 0
        self.last_animation_update = pygame.time.get_ticks()

    def _setup_physics(self):
        """Configure physics-related properties"""
        self.move_speed = MOVE_SPEED
        self.jump_strength = JUMP_STRENGTH
        self.gravity = GRAVITY
        self.max_fall_speed = MAX_FALL_SPEED
        self.fast_fall_speed = FAST_FALL_SPEED

    def handle_input(self, keys):
        """Process player input and update state"""
        self._handle_movement(keys)
        self._handle_jumping(keys)
        self._handle_attacks(keys)

    def _handle_movement(self, keys):
        """Process horizontal movement input"""
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.move_speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = self.move_speed
            self.facing_right = True

    def _handle_jumping(self, keys):
        """Process jump and fast fall input"""
        if keys[pygame.K_UP] and not self.jumping:
            self.velocity.y = self.jump_strength
            self.jumping = True

        if keys[pygame.K_DOWN] and self.jumping:
            self.velocity.y = self.fast_fall_speed

    def _handle_attacks(self, keys):
        if keys[pygame.K_a]:
            self._perform_attack(SoundKey.SWORD)
            if self.attacking is None:
                self.attacking = FighterActionNUM.ATK1
                self.current_frame = 0
                self.last_animation_update = pygame.time.get_ticks()
        elif keys[pygame.K_d]:
            self._perform_attack(SoundKey.SWORD)
            if self.attacking is None:
                self.attacking = FighterActionNUM.ATK2
                self.current_frame = 0
                self.last_animation_update = pygame.time.get_ticks()

    def _get_current_frame(self):
        """Get properly oriented animation frame"""
        frames = self.animations[self.current_action]
        """
        ensures the current frames is not exceeded (frame = self.animations[JUMP][7])!, JUMP has only 3 frames
        (IndexError: list index out of range) not matching animations with frames length

        """
        if self.current_frame >= len(frames):
            self.current_frame = 0

        frame = self.animations[self.current_action][self.current_frame]
        surf = pygame.transform.flip(frame, not self.facing_right, False)
        return surf

    def _apply_physics(self):
        """Apply physics calculations"""
        # Horizontal movement
        self.player_position.x += self.velocity.x
        self.player_position.x = max(0, min(int(self.player_position.x), self.bg_width - 100))

        # Vertical movement
        self.velocity.y += self.gravity
        self.velocity.y = min(self.velocity.y, self.max_fall_speed)
        self.player_position.y += self.velocity.y

        # Ground collision
        if self.player_position.y >= self.bg_height - 200:
            self.player_position.y = self.bg_height - 200
            self.velocity.y = 0
            self.jumping = False

    def update(self):
        """Update player state and physics"""
        self._apply_physics()
        self._update_action_state()
        self._update_animation()
        self._update_rect()

    def _update_action_state(self):
        # 1) Attack has top priority
        if self.attacking is not None:
            # fetch all frames for this attack
            frames = self.animations[self.attacking]
            # if we haven’t finished the attack animation yet:
            if self.current_frame < len(frames) - 1:
                self.current_action = self.attacking
                return
            # otherwise, attack is done:
            self.attacking = None

        # 2) In the air?
        if self.jumping:
            self.current_action = FighterActionNUM.RUN if self.velocity.x else FighterActionNUM.JUMP
            return

        # 3) On ground and moving?
        if self.velocity.x:
            self.current_action = FighterActionNUM.RUN
            return

        # 4) Default to idle
        self.current_action = FighterActionNUM.IDLE

    def _update_animation(self):
        """Update animation frame based on state"""
        now = pygame.time.get_ticks()
        if now - self.last_animation_update > FRAME_DURATION:
            self.last_animation_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_action])

    def _perform_attack(self, sound_key):
        """Execute attack logic"""
        if self.attacking in [FighterActionNUM.ATK1, FighterActionNUM.ATK2]:
            self.game.audio.play_sfx(sound_key)

    def _update_rect(self):
        if self.current_action in [FighterActionNUM.ATK1, FighterActionNUM.ATK2]:
            new_w = self.rect_size.x + PLAYER_ATK_RECT_W
            new_h = self.rect_size.y
        else:
            new_w = self.rect_size.x
            new_h = self.rect_size.y

        # 1) resize in place
        self.rect.size = (new_w, new_h)

        # 2) reposition so its top-left matches your logical player_position
        if self.facing_right:
            self.rect.topleft = (
                self.player_position.x,
                self.player_position.y
            )
        else:
            self.rect.topright = (
                self.player_position.x + PLAYER_ATK_RECT_W,
                self.player_position.y
            )

    def draw(self):
        player_screen = self._get_current_frame()

        self.game.screen.blit(player_screen, (
            self.player_position.x - (PLAYER_OFFSET[0] * PLAYER_SCALE),
            self.player_position.y - (PLAYER_OFFSET[1] * PLAYER_SCALE)
        ))
        if DEBUG:
            pygame.draw.rect(self.game.screen, (0, 0, 0), self.player_rect, 2)

    def is_alive(self):
        return self.alive

    def check_collision_with_enemy(self, enemy_rect):
        return self.player_rect.colliderect(enemy_rect)

    @property
    def player_rect(self):
        return self.rect
