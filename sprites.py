

import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)
from pygame.transform import rotozoom

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self, size: float, move_rate: float, screen_height: int, screen_width: int):
        super(Player, self).__init__()
        self.surf = rotozoom(pygame.image.load("art/RocketWhiteSideR.png").convert_alpha(), angle=0, scale=size*2)
        self.move_rate = move_rate
        self.rect = self.surf.get_rect(center=(40, screen_height / 2))  # start in middle of screen
        self.height_lim = screen_height
        self.width_lim = screen_width
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.move_rate)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.move_rate)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.move_rate, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.move_rate, 0)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.width_lim:
            self.rect.right = self.width_lim
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.height_lim:
            self.rect.bottom = self.height_lim