import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
CHARACTER_COLOR = (0, 0, 0)
CHARACTER_RADIUS = 20
VELOCITY = 1

# Character position and target position
character_x, character_y = WIDTH // 2, HEIGHT // 2
target_x, target_y = character_x, character_y
moving = False

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clickable Character Movement")

def lerp(start, end, t):
    return start + t * (end - start)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            target_x, target_y = pygame.mouse.get_pos()
            moving = True

    if moving:
        distance = math.hypot(target_x - character_x, target_y - character_y)
        if distance > 1:
            t = VELOCITY / distance
            character_x = lerp(character_x, target_x, t)
            character_y = lerp(character_y, target_y, t)
        else:
            moving = False

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw the character
    pygame.draw.circle(screen, CHARACTER_COLOR, (int(character_x), int(character_y)), CHARACTER_RADIUS)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
