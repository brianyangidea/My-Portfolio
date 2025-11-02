#This program is used to run the loading screen


import pygame
import sys
import random
import math
import time

def run_loading_screen():
    #Initializes Pygame
    pygame.init()

    #Screen settings
    WIDTH, HEIGHT = 1000, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Now Loading...")

    #Clock to control frame rate
    clock = pygame.time.Clock()

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Text setup
    font = pygame.font.Font(None, 32)
    text = "Booting up system..."

    # Square setup
    square_size = 100
    angle = 0

    # Flashing text & color timing
    color_change_time = 0
    current_color = WHITE

    # Bar graph settings
    num_bars = 40
    bar_width = WIDTH // num_bars
    max_bar_height = 160
    min_bar_height = 5

    # Create bar data
    bars = []
    count = 0
    for _ in range(num_bars):
        height = random.randint(20, max_bar_height)
        bars.append({
            "height": height,
            "target": random.randint(min_bar_height, max_bar_height),
            "color": (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))})

    # Timer to pick new targets for bars
    CHANGE_INTERVAL = 2000  # ms
    last_change = pygame.time.get_ticks()

    # Smooth animation speed
    SPEED = 0.05  # 0.0–1.0, larger = faster motion

    # Load the image amnd set it
    image = pygame.image.load("lab_logo.png")
    image = pygame.transform.scale(image, (288.5, 27))
    image_rect = image.get_rect(topleft=(20, 20))

    # A list of stupid loading strings to choose from for comedic effect
    first_half_strings = ["Re-routing",
                        "Typing up",
                        "Downloading",
                        "Installing",
                        "Creating",
                        "Saving",
                        "Hacking",
                        "Uploading",
                        "Booting up",
                        "Debugging",
                        "Coding",
                        "Complexifying",
                        "Searching up",
                        "Copying",
                        "Formatting",
                        "Fixing",
                        "Moving",
                        "Reading",
                        "Updating",
                        "Getting",
                        "Invoking",
                        "Retrieving",
                        "Supporting",
                        "Adding",
                        "Obtaining",
                        "Organizing",
                        "Executing",
                        "Programming",
                        "Writing"
                        
    ]
    second_half_strings = ["a bunch of computer hardware",
                        "copious amounts of microchips",
                        "very complex stuff, I assure you",
                        "stuff that is really cool",
                        "random computer updates",
                        "a lot of binary code",
                        "proper coding conventions",
                        "a really messy computer desktop",
                        "a barely-contained NULL statement",
                        "extremely obscure programming facts",
                        "a lot of useful functions",
                        "a keen sense of optimism",
                        "a mountain of cat pictures",
                        "way too many if-else statements",
                        "many sleepless nights of coding",
                        "computer updates that just won't finish",
                        "a fun attitude with a sense of humour to match",
                        "the greatest coding project you've ever seen",
                        "robot stuff. Beep boop! Yep",
                        "a hip, new loading screen",
                        "computer stuff that shouldn't be touched",
                        "a childlike sense of wonder",
                        "hardworking, loyal morals",
                        "intrusive thoughts about functions",
                        "bits and bytes and bits and bytes",
                        "nothing in particular",
                        "something REAAAAALLLYY important",
                        "an inside joke between me, myself, and I",
                        "a stable, expertly-coded blockchain",
                        "something really funny. You wouldn't get it",
                        "something. Don't know what, just something",
                        "exactly 1000 lines of codes and not one more",
                        "a random desire to make something fun"

                        
    ]

    # Add any single piece strings you want to the pool (these will come up super rarely!)
    strings = ["This is a super rare message. If you see it, congrats!"]

    # Combine strings from both lists
    for item1 in first_half_strings:
        for item2 in second_half_strings:
            strings.append(item1 + " " + item2 + "...")  # combine with a space


    # Main loop
    start_time = time.time()
    duration = 999  # seconds

    while time.time() - start_time < duration:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update angle for rotation
        angle += 2  # degrees per frame
        if angle >= 360:
            angle = 0

        # Update text color every few seconds
        current_time = pygame.time.get_ticks()
        if current_time - color_change_time > 2000:
            color_change_time = current_time
            current_color = (
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255)
            )
            text = random.choice(strings)

        # Clear screen
        screen.fill(BLACK)

        # Render flashing text
        text_surface = font.render(text, True, current_color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(text_surface, text_rect)

        #Render logo image
        screen.blit(image, image_rect)

        # Create and rotate square
        square_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        pygame.draw.rect(square_surface, current_color, (0, 0, square_size, square_size))
        rotated_square = pygame.transform.rotate(square_surface, angle)
        rect = rotated_square.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        # Draw square
        screen.blit(rotated_square, rect)

        # Time handling for target updates
        now = pygame.time.get_ticks()
        if now - last_change > CHANGE_INTERVAL:
            last_change = now
            for bar in bars:
                bar["target"] = random.randint(20, max_bar_height)

        # Smoothly move current height toward target
        for bar in bars:
            bar["height"] += (bar["target"] - bar["height"]) * SPEED

        # Draw bars
        for i, bar in enumerate(bars):
            x = i * bar_width
            y = HEIGHT - bar["height"]
            pygame.draw.rect(screen, bar["color"], (x, y, bar_width - 2, bar["height"]))

        # Update display
        pygame.display.flip()

        # Cap frame rate
        clock.tick(60)

    pygame.quit()

