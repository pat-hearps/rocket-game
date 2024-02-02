import random

import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)
from pygame.transform import rotozoom

from utils import scale_variable

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


# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
enemy_art = {
    1 : "BluePlanet.png",
    2 : "FullMoon.png",
    3 : "PurplePlanet.png",
    4 : "RedPlanet.png",
    5 : "Earth.png",
    6 : "Hurricane.png",
    7 : "RedMoon.png"
}
class Enemy(pygame.sprite.Sprite):
    def __init__(self, size: float, screen_height: int, screen_width: int, difficulty_scaler: float):
        super(Enemy, self).__init__()
        self.size = size
        self.height_lim = screen_height
        self.width_lim = screen_width
        self.id = random.randint(1, 7)
        self.speed =  scale_variable(self.id, inverse_difficulty=difficulty_scaler)

        self.surf = rotozoom(pygame.image.load(f"art/{enemy_art[self.id]}").convert_alpha(), angle=0, scale=self.size)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(self.width_lim + 20, self.width_lim + 100),  # spawns somewhere off right edge of screen, random distance
                random.randint(0, self.height_lim),  # spawns somewhere between bottom and top of screen
            )
        )

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
