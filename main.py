import argparse
import math


import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from pygame.transform import rotozoom

from sprites import Player, Enemy

ROCKET_MOVE_RATE = 4
SPRITE_SIZE = 2
BASE_NME_SPEED = 5.0  # pixels / frame
BASE_NME_SPAWN_RATE = 400.0  # milliseconds between spawns

# Define constants for the screen width and height
SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 800


def main(difficulty: int):

    checked_difficulty = max(min(difficulty, 10), 1)  # enforce between 1-10
    inverse_difficulty = 10 - checked_difficulty

    print(f"running at difficulty = {difficulty}  (inverse = {inverse_difficulty})")
    pygame.init()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Set up scrolling background images
    background = rotozoom(pygame.image.load("./art/Green Nebula 4 - 512x512.png").convert(), angle=0, scale=1)
    bg_width = background.get_width()
    bg_height = background.get_height()

    # HERE 1 IS THE CONSTANT FOR REMOVING BUFFERING - change to higher number if you get buffering of the imager
    n_tiles_scrolling = math.ceil(SCREEN_HEIGHT / bg_height) + 1
    n_tiles_across = math.ceil(SCREEN_WIDTH / bg_width)  # how many tiles to stitch together to fill the screen, don't need extra
    scroll = 0  # start of background scrolling
    scroll_rate = 1.5

    # Create a custom event for adding a new enemy
    ADDENEMY = pygame.USEREVENT + 1  # just the last reserved event, plus 1
    spawn_freq = inverse_difficulty * 150 + 100
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
        while(i < n_tiles_scrolling):
            for t in range(n_tiles_across):
                screen.blit(background, dest=(t * bg_height, bg_width * i + scroll)) 
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
                new_enemy = Enemy(size=SPRITE_SIZE, screen_height=SCREEN_HEIGHT, screen_width=SCREEN_WIDTH, difficulty_scaler=inverse_difficulty)
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--difficulty","-d", type=int, default=4)
    args = parser.parse_args()
    difficulty = args.difficulty
    main(difficulty)
