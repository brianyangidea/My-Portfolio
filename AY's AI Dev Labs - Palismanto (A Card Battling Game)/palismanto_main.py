import pygame
import sys
import vlc
import time

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Palismanto: The Card Battling Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
LIGHT_BLUE = (100, 160, 210)
GREEN = (50, 180, 100)
RED = "red"

# Fonts
font_large = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 36)

# --- Base Screen Class ---
class Screen:
    def __init__(self, manager):
        self.manager = manager  # Reference to the ScreenManager

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass

# --- Title Screen ---
class TitleScreen(Screen):

    def __init__(self, manager):
        super().__init__(manager)
        self.button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        self.soundtrack = play_mp3("royalty_free_music/Palismanto_Title_Card.mp3", volume=80)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.soundtrack.stop()
                self.soundtrack = play_mp3("royalty_free_music/Palismanto_Stinger.mp3", volume=80)
                time.sleep(2.2)
                self.manager.go_to(GameScreen(self.manager))
                self.soundtrack.stop()

    def draw(self, surface):
        surface.fill(WHITE)
        title_text = font_large.render("Palismanto: The Card Battling Game", True, BLACK)
        surface.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

        # Draw button
        mouse_pos = pygame.mouse.get_pos()
        color = LIGHT_BLUE if self.button_rect.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(surface, color, self.button_rect)
        button_text = font_small.render("Start Game", True, WHITE)
        surface.blit(button_text, (self.button_rect.centerx - button_text.get_width() // 2,
                                   self.button_rect.centery - button_text.get_height() // 2))
        
    def draw_transition(self, surface):
        surface.fill(RED)
        title_text = font_large.render("Palismanto: The Card Battling Game", True, BLACK)
        surface.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

        # Draw button
        mouse_pos = pygame.mouse.get_pos()
        color = LIGHT_BLUE if self.button_rect.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(surface, color, self.button_rect)
        button_text = font_small.render("Start Game", True, WHITE)
        surface.blit(button_text, (self.button_rect.centerx - button_text.get_width() // 2,
                                   self.button_rect.centery - button_text.get_height() // 2)) 


# --- Game Screen ---
class GameScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.go_to(TitleScreen(self.manager))  # Go back to title

    def draw(self, surface):
        surface.fill(GREEN)
        text = font_large.render("Game Screen", True, WHITE)
        surface.blit(text, (WIDTH // 2 - text.get_width() // 2,
                            HEIGHT // 2 - text.get_height() // 2))

        info = font_small.render("Press ESC to return", True, WHITE)
        surface.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 2 + 50))


# --- Screen Manager ---
class ScreenManager:
    def __init__(self):
        self.current_screen = TitleScreen(self)

    def go_to(self, screen):
        self.current_screen = screen

    def handle_event(self, event):
        self.current_screen.handle_event(event)

    def update(self):
        self.current_screen.update()

    def draw(self, surface):
        self.current_screen.draw(surface)


def play_mp3(file_path, volume=100):
    """
    Plays an MP3 file in a non-blocking loop using VLC.
    
    Parameters:
        file_path (str): Path to the MP3 file
        volume (int): Volume (0–100)
    
    Returns:
        player (vlc.MediaPlayer): The VLC player object, so you can stop it later
    """
    # Create VLC instance
    instance = vlc.Instance("--input-repeat=-1")  # -1 = infinite loop
    player = instance.media_player_new()

    # Load file and set up
    media = instance.media_new(file_path)
    player.set_media(media)
    player.audio_set_volume(volume)

    # Play the music (non-blocking)
    player.play()

    print(f"🎶 Now looping '{file_path}' at volume {volume}% (non-blocking)")
    return player


# --- Main Loop ---
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
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
