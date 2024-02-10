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


class Game:
    def __init__(self, inverse_difficulty: int, screen: pygame.Surface, scroll_rate: float = 1.5):
        self.screen = screen

        # Set up scrolling background images
        self.background = rotozoom(pygame.image.load("./art/Green Nebula 4 - 512x512.png").convert(), angle=0, scale=SPRITE_SIZE)
        self.bg_width = self.background.get_width()
        self.bg_height = self.background.get_height()
        self.scroll_rate = scroll_rate
        self.inverse_difficulty = inverse_difficulty
        

        # HERE 1 IS THE CONSTANT FOR REMOVING BUFFERING - change to higher number if you get buffering of the imager
        self.n_tiles_scrolling = math.ceil(SCREEN_HEIGHT / self.bg_height) + 1
        self.n_tiles_across = math.ceil(SCREEN_WIDTH / self.bg_width)  # how many tiles to stitch together to fill the screen, don't need extra
        print(f"using {self.n_tiles_across} tiles across, {self.n_tiles_scrolling} for scrolling")
        
    

        # Create a custom event for adding a new enemy
        self.ADDENEMY = pygame.USEREVENT + 1  # just the last reserved event, plus 1
        self.spawn_freq = inverse_difficulty * 150 + 100
        print(f"spawning enemies every {self.spawn_freq} millis")
        
    def play_game(self):    
        self.scroll = 0  # start of background scrolling
        
        pygame.time.set_timer(self.ADDENEMY, millis=self.spawn_freq)  # spawn every {freq} milliseconds

        # Instantiate player. Right now, this is just a rectangle.
        self.player = Player(size=SPRITE_SIZE, move_rate=ROCKET_MOVE_RATE, screen_height=SCREEN_HEIGHT, screen_width=SCREEN_WIDTH)

        # Create groups to hold enemy sprites and all sprites
        # - enemies is used for collision detection and position updates
        # - all_sprites is used for rendering
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Setup the clock for a decent framerate - before game loop begins
        self.clock = pygame.time.Clock()

        run = True
        while run:
            # append background image to front of same image

            for i in range(self.n_tiles_scrolling):
                for t in range(self.n_tiles_across):
                    self.screen.blit(self.background, dest=(t * self.bg_width, -self.bg_height * i + self.scroll)) 

            # FRAMERATE FOR SCROLLING 
            self.scroll += self.scroll_rate
        
            # RESET THE SCROLL FRAME 
            if abs(self.scroll) > self.bg_height: 
                self.scroll = 0

            # Look at every event in the queue
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == KEYDOWN:
                    # Was it the Escape key? If so, stop the loop.
                    if event.key == K_ESCAPE:
                        run = False
                        # Add a new enemy?
                elif event.type == self.ADDENEMY:
                    # Create the new enemy and add it to sprite groups
                    new_enemy = Enemy(size=SPRITE_SIZE, screen_height=SCREEN_HEIGHT, screen_width=SCREEN_WIDTH, difficulty_scaler=inverse_difficulty)
                    self.enemies.add(new_enemy)
                    self.all_sprites.add(new_enemy)

                # Did the user click the window close button? If so, stop the loop.
                elif event.type == QUIT:
                    run = False

            pressed_keys: dict = pygame.key.get_pressed()
            self.player.update(pressed_keys)

            # Update all enemy positions
            self.enemies.update()  # calls self.update() method on all enemy sprites in the group

            # Redraw all sprites including player
            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            # Check if any enemies have collided with the player
            if pygame.sprite.spritecollideany(self.player, self.enemies):
                # If so, then remove the player and stop the loop
                self.player.kill()
                run = False

            # Draw the player on the screen
            self.screen.blit(self.player.surf, self.player.rect)

            # Flip the display
            pygame.display.flip()

            # Last step in loop - ensure program maintains desired frame rate of X frames per second
            self.clock.tick(60)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--difficulty","-d", type=int, default=4)
    args = parser.parse_args()
    difficulty = args.difficulty


    checked_difficulty = max(min(difficulty, 10), 1)  # enforce between 1-10
    inverse_difficulty = 10 - checked_difficulty

    print(f"running at difficulty = {difficulty}  (inverse = {inverse_difficulty})")
    
    pygame.init()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    game = Game(inverse_difficulty, screen)

    game.play_game()

    # Done! Time to quit.
    pygame.quit()
