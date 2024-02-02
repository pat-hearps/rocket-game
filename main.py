import argparse
import math
import random

import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from pygame.transform import rotozoom

from sprites import Player

ROCKET_MOVE_RATE = 4
SPRITE_SIZE = 2

parser = argparse.ArgumentParser()
parser.add_argument("--difficulty","-d", type=int, default=4)
args = parser.parse_args()
difficulty = args.difficulty

BASE_NME_SPEED = 5.0  # pixels / frame
BASE_NME_SPAWN_RATE = 400.0  # milliseconds between spawns
checked_difficulty = max(min(difficulty, 10), 1)  # enforce between 1-10
INVERSE_DIFFICULTY = 10 - checked_difficulty

print(f"running at difficulty = {difficulty}  (inverse = {INVERSE_DIFFICULTY})")

def scale_variable(variable, inverse_difficulty=INVERSE_DIFFICULTY):
    """applies slightly non-linear increasing scale to speed etc based on difficulty level"""
    return variable * (2 * (1.25 ** -inverse_difficulty))

# Define constants for the screen width and height
SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 800

pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set up scrolling background images
background = rotozoom(pygame.image.load("./art/Green Nebula 4 - 512x512.png").convert(), angle=0, scale=SPRITE_SIZE)
bg_width = background.get_width()

# HERE 1 IS THE CONSTANT FOR REMOVING BUFFERING - change to higher number if you get buffering of the imager
n_tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1
scroll = 0  # start of background scrolling
scroll_rate = 1.5




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
    def __init__(self):
        super(Enemy, self).__init__()
        self.id = random.randint(1, 7)
        self.speed =  scale_variable(self.id)
        # self.surf = pygame.Surface((20, 10))
        # self.surf.fill((170, 170, 170))
        self.surf = rotozoom(pygame.image.load(f"art/{enemy_art[self.id]}").convert_alpha(), angle=0, scale=SPRITE_SIZE)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),  # spawns somewhere off right edge of screen, random distance
                random.randint(0, SCREEN_HEIGHT),  # spawns somewhere between bottom and top of screen
            )
        )
        

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1  # just the last reserved event, plus 1
spawn_freq = INVERSE_DIFFICULTY * 150 + 100
print(f"spawning enemies every {spawn_freq} millis")
pygame.time.set_timer(ADDENEMY, millis=spawn_freq)  # spawn every {freq} milliseconds

# Instantiate player. Right now, this is just a rectangle.
player = Player(size=SPRITE_SIZE, move_rate=ROCKET_MOVE_RATE, screen_height=SCREEN_HEIGHT, screen_width=SCREEN_WIDTH)

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Setup the clock for a decent framerate - before game loop begins
clock = pygame.time.Clock()

run = True
while run:
    # append background image to front of same image
    i = 0
    while(i < n_tiles): 
        screen.blit(background, dest=(bg_width * i + scroll, 0)) 
        i += 1
    # FRAMERATE FOR SCROLLING 
    scroll -= scroll_rate
  
    # RESET THE SCROLL FRAME 
    if abs(scroll) > bg_width: 
        scroll = 0

    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                run = False
                # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            run = False

    pressed_keys: dict = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update all enemy positions
    enemies.update()  # calls self.update() method on all enemy sprites in the group

    # Redraw all sprites including player
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        run = False

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    # Flip the display
    pygame.display.flip()

    # Last step in loop - ensure program maintains desired frame rate of X frames per second
    clock.tick(60)

# Done! Time to quit.
pygame.quit()