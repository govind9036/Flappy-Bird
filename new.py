import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((500, 500))

# Try loading the image
try:
    powerup_image = pygame.image.load('gallery/sprites/powerup.png')
except pygame.error as e:
    print(f"Failed to load image: {e}")
    sys.exit()

# Display the image for testing
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen and display the image at a position
    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(powerup_image, (200, 200))  # Draw the image at (200, 200)
    pygame.display.update()

pygame.quit()
