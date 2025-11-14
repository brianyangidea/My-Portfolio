import screens.screens
import pygame
import sys
import vlc
import time

# This file contains and handles all the various screens used in the program
from screens.screens import ScreenManager

# Screen setup
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Palismanto: A D&D-Inspired Card Battling Game')
pygame.mouse.set_visible(False)


# Main Loop
def main():
    clock = pygame.time.Clock()
    manager = ScreenManager()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            manager.handle_event(event)

        manager.update()
        manager.draw(screen)

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Draw smiley face
        face_radius = 10
        pygame.draw.circle(screen, "YELLOW", (mouse_x, mouse_y), face_radius)
        pygame.draw.circle(screen, "BLACK", (mouse_x, mouse_y), face_radius, 2)
        eye_offset_x = 2
        eye_offset_y = 4
        pygame.draw.circle(screen, "BLACK", (mouse_x - eye_offset_x, mouse_y - eye_offset_y), 1)
        pygame.draw.circle(screen, "BLACK", (mouse_x + eye_offset_x, mouse_y - eye_offset_y), 1)
        smile_rect = pygame.Rect(mouse_x - 5, mouse_y - 5, 10, 10)
        pygame.draw.arc(screen, "BLACK", smile_rect, 3.14, 6.28, 1)

        # Handle pygame clock
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
