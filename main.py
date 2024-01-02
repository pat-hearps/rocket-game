import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

run = True
while run:
    
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                run = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            run = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    ## Create a surface and pass in a tuple containing its length and width
    surf = pygame.Surface((50, 50))

    # Give the surface a color to separate it from the background
    surf.fill((0, 0, 0))
    rect = surf.get_rect()

    # This says "Draw surf onto the screen at the center"
    # Put the center of surf at the center of the display
    surf_center = (
        (SCREEN_WIDTH-surf.get_width())/2,
        (SCREEN_HEIGHT-surf.get_height())/2
    )
    # Draw surf at the new coordinates
    screen.blit(surf, surf_center)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()