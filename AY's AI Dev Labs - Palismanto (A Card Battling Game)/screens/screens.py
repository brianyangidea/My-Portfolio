# Colors
import pygame
import sys
import vlc
import time
import random
import math

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 640, 480

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
LIGHT_BLUE = (100, 160, 210)
GREEN = (50, 180, 100)
RED = "red"

# Fonts
font_large = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 36)
font_verysmall = pygame.font.SysFont(None, 24)

# Base Screen Class
class Screen:
    def __init__(self, manager):
        self.manager = manager  # Reference to the ScreenManager

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass

# Title Screen
class TitleScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)
        self.button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        self.soundtrack = play_mp3("royalty_free_music/Palismanto_Title_Card.mp3", volume=80)
        
        # Bouncing squares state array
        self.squares = []

        # Base square variables (for preservation)
        self.squares.append({
            'size': 40,
            'pos': [50.0, 50.0],
            'vel': [2.4, 1.8],
            'color': (200, 60, 60),
        })
        # Add in 14 more random squares for 15 total
        for _ in range(14):
            size = random.randint(24, 68)
            x = random.uniform(0, WIDTH - size)
            y = random.uniform(0, HEIGHT - size)
            vx = random.choice([-1, 1]) * random.uniform(1.2, 3.0)
            vy = random.choice([-1, 1]) * random.uniform(1.0, 2.8)
            color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            self.squares.append({
                'size': size,
                'pos': [x, y],
                'vel': [vx, vy],
                'color': color,
            })

    def update(self):
        # Update all squares
        for s in self.squares:
            s['pos'][0] += s['vel'][0]
            s['pos'][1] += s['vel'][1]

            # Bounce off left/right
            if s['pos'][0] <= 0:
                s['pos'][0] = 0
                s['vel'][0] = abs(s['vel'][0])
                # changed color on bounce
                s['color'] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            elif s['pos'][0] + s['size'] >= WIDTH:
                s['pos'][0] = WIDTH - s['size']
                s['vel'][0] = -abs(s['vel'][0])
                s['color'] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

            # Bounce off top/bottom
            if s['pos'][1] <= 0:
                s['pos'][1] = 0
                s['vel'][1] = abs(s['vel'][1])
                s['color'] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            elif s['pos'][1] + s['size'] >= HEIGHT:
                s['pos'][1] = HEIGHT - s['size']
                s['vel'][1] = -abs(s['vel'][1])
                s['color'] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.soundtrack.stop()
                self.soundtrack = play_mp3("royalty_free_music/Palismanto_Stinger.mp3", volume=80)
                time.sleep(2.2)
                self.manager.go_to(GameScreen(self.manager))

    def draw(self, surface):
        surface.fill(WHITE)
        # Draw all bouncing squares
        for s in self.squares:
            pygame.draw.rect(surface, s['color'],
                             (int(s['pos'][0]), int(s['pos'][1]), s['size'], s['size']))
        title_text = font_large.render("Palismanto: The Card Battling Game", True, BLACK)
        surface.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

        # Draw button
        mouse_pos = pygame.mouse.get_pos()
        color = LIGHT_BLUE if self.button_rect.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(surface, color, self.button_rect)
        button_text = font_small.render("Start Game", True, WHITE)
        surface.blit(button_text, (self.button_rect.centerx - button_text.get_width() // 2,
                                   self.button_rect.centery - button_text.get_height() // 2))
    # (squares already drawn behind UI)


# Game Screen
class GameScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)
        self.soundtrack = play_mp3("royalty_free_music/Palismanto_Menu.mp3", volume=80)

        # Animated bars at the bottom
        self.bar_count = 8
        self.bar_width = max(8, WIDTH // (self.bar_count * 3))
        self.bar_spacing = self.bar_width // 2
        self.bar_max_height = 120
        # Per-bar attributes (phase, speed, color)
        self.bars = []
        for i in range(self.bar_count):
            phase = i * (2 * math.pi / max(1, self.bar_count))
            speed = 0.8 + (i % 4) * 0.25
            c = pygame.Color(0, 0, 0)
            c.hsva = (i * (360 / max(1, self.bar_count)), 75, 85, 100)
            color = (c.r, c.g, c.b)
            self.bars.append({'phase': phase, 'speed': speed, 'color': color})
        self.bar_time = 0.0

    def update(self):
        # advance animation time for bars
        self.bar_time += 0.06

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.go_to(TitleScreen(self.manager))  # Go back to title
            self.soundtrack.stop()

    def draw(self, surface):
        surface.fill(GREEN)
        text = font_large.render("Welcome To A New Adventure!", True, WHITE)
        surface.blit(text, (WIDTH // 2 - text.get_width() // 2,
                            HEIGHT // 6 - text.get_height() // 6))
        
        info = font_small.render("Make a selection:", True, WHITE)
        surface.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 6 + 50))

        info = font_verysmall.render("Press ENTER to start!", True, WHITE)
        surface.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 6 + 100))

        info = font_verysmall.render("Press SPACE to adjust settings?", True, WHITE)
        surface.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 6 + 150))

        info = font_verysmall.render("Or press ESC to return...", True, WHITE)
        surface.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 6 + 200))

        # Draw animated multicolored bars at the bottom
        total_width = self.bar_count * self.bar_width + (self.bar_count - 1) * self.bar_spacing
        start_x = (WIDTH - total_width) // 2
        bottom_margin = 12
        for i, bar in enumerate(self.bars):
            h = (math.sin(self.bar_time * bar['speed'] + bar['phase']) + 1) / 2
            height = int(h * self.bar_max_height)
            x = start_x + i * (self.bar_width + self.bar_spacing)
            y = HEIGHT - bottom_margin - height
            rect = pygame.Rect(x, y, self.bar_width, height)
            pygame.draw.rect(surface, bar['color'], rect)


# Screen Manager
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

# Function to play mp3 
def play_mp3(file_path, volume=100):
    """
    Plays an MP3 file in a non-blocking loop using VLC.
    
    - file_path (str): Path to the MP3 file
    - volume (int): Volume (0–100)
    
    Returns player (vlc.MediaPlayer), the VLC player object, so you can stop it later
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

    return player