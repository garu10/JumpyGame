import pygame
import sys
from main import JumpingGame
from scoreboard import Scoreboard

pygame.init()
FONT = pygame.font.Font(None, 36)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

WHITE = (255, 255, 255)
BLUE = (0, 0, 225)
NAVY_BLUE = (0, 0, 128)

# Load images
BACKGROUND_IMAGE = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/bgmain.png")
LOGO_IMAGE = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/1.png")
HIGH_SCORE = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/2.png")
START_BUTTON = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/3.png")
SETTINGS_BUTTON = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/4.png")
HOME_BUTTON = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/6.png")
DESCRIPTION_BUTTON = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/31.png")
SETTINGS_LOGO_IMAGE = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/1.png")
bg_music = pygame.mixer.Sound("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/funky-and-jazzy-gang-loop-275533.mp3")

# Scale images
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
LOGO_IMAGE = pygame.transform.scale(LOGO_IMAGE, (600, 450))
HIGH_SCORE = pygame.transform.scale(HIGH_SCORE, (400, 200))
START_BUTTON = pygame.transform.scale(START_BUTTON, (150, 200))
SETTINGS_BUTTON = pygame.transform.scale(SETTINGS_BUTTON, (150, 200))
HOME_BUTTON = pygame.transform.scale(HOME_BUTTON, (500, 500))
DESCRIPTION_BUTTON = pygame.transform.scale(DESCRIPTION_BUTTON, (500, 500))
SETTINGS_LOGO_IMAGE = pygame.transform.scale(SETTINGS_LOGO_IMAGE, (300, 200))

class Button:
    def __init__(self, image, x, y, width, height, action=None, volume=None):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.action = action
        self.volume = volume  # Store the volume parameter

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            if callable(self.action):
                if self.volume is not None:  # Check if volume is passed
                    self.action(self.volume)  # Pass volume to the action
                else:
                    self.action()  # If no volume is needed, just call the action
            elif self.action == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

class Slider:
    def __init__(self, x, y, width, height, min_value=0, max_value=1, initial_value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.knob_rect = pygame.Rect(x, y, height, height)  # Knob size is square, same height as slider
        self.knob_rect.centerx = x + int(width * self.value)

    def draw(self, screen):
        # Draw the slider bar
        pygame.draw.rect(screen, BLUE, self.rect)
        # Draw the knob
        pygame.draw.rect(screen, WHITE, self.knob_rect)

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            # Update the knob position based on the mouse's x position
            offset = mouse_pos[0] - self.rect.left
            self.value = (offset / self.rect.width)
            self.value = max(min(self.value, 1), 0)  # Clamp value to [0, 1]
            self.knob_rect.centerx = self.rect.left + int(self.rect.width * self.value)

    def get_value(self):
        return self.value

def start_game(volume):
    # Start the JumpingGame instance and run the game
    print(f"Starting game with volume: {volume}")  # For debugging
    bg_music.set_volume(0)
    bg_music.stop()
    jumping_game = JumpingGame(volume)
    jumping_game.run_game()

def open_description():
    description_running = True

    # Function to go back to settings
    def go_back():
        nonlocal description_running
        description_running = False  # Close the description screen

    # Button to return to settings
    back_button = Button(HOME_BUTTON, SCREEN_WIDTH - 170, 10, 230, 100, go_back)

    while description_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                back_button.check_click(mouse_pos)

        image = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/main interface (1).png')  # Replace with the actual image path
        image = pygame.transform.scale(image, (500, 700))
        # Display the background image
        screen.blit(image, (0, 0))  # Blit the image to the top-left corner of the screen

        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def open_settings(volume):
    settings_running = True
    slider = Slider(100, 400, 300, 20, min_value=0, max_value=1, initial_value=volume)  # Volume slider

    def go_home():
        nonlocal settings_running
        settings_running = False
    def show_description():
        open_description()

    home_button = Button(HOME_BUTTON, SCREEN_WIDTH - 170, 10, 230, 100, go_home)
    description_button = Button(DESCRIPTION_BUTTON, SCREEN_WIDTH // 2 - 300, 12, 200, 100, show_description)  # Description button
    logo_rect = SETTINGS_LOGO_IMAGE.get_rect(center=(SCREEN_WIDTH // 2, 150))


    # Load and play music
    # pygame.mixer.music.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/Doodle Jump Monster Sound.mp3")
    # pygame.mixer.music.play(-1, 0.0)

    while settings_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                home_button.check_click(mouse_pos)
                description_button.check_click(mouse_pos)  # Check if description button is clicked
                slider.update(mouse_pos)  # Update slider on mouse click

        # Get the volume value from the slider
        volume = slider.get_value()
        bg_music.set_volume(volume)  # Set the game volume

        screen.blit(BACKGROUND_IMAGE, (0, 0))
        settings_text = FONT.render("Volume", True, BLUE)
        screen.blit(settings_text, (SCREEN_WIDTH // 2 - settings_text.get_width() // 2, 350))

        screen.blit(SETTINGS_LOGO_IMAGE, logo_rect)

        # Draw the slider
        slider.draw(screen)

        home_button.draw(screen)
        description_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    return volume  # Return the updated volume after exiting settings

def main():
    global screen, clock, volume
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Menu")
    clock = pygame.time.Clock()

    # Initialize volume with a default value
    volume = 0.5  # Default volume value

    # Initialize the Scoreboard
    class MockGame:  # Mock game object for Scoreboard
        def __init__(self, screen):
            self.screen = screen

    game = MockGame(screen)
    scoreboard = Scoreboard(game)

    # Buttons for start and settings
    start_button = Button(START_BUTTON, SCREEN_WIDTH // 2 - 100, 400, 200, 150, lambda: start_game(volume))
    settings_button = Button(SETTINGS_BUTTON, SCREEN_WIDTH // 2 - 100, 500, 200, 150, lambda: open_settings(volume))

    settings_active = False  # Flag to track if settings screen is active

    running = True
    while running:
        bg_music.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                start_button.check_click(mouse_pos)  # Pass the volume when start button is clicked
                if settings_button.rect.collidepoint(mouse_pos):
                    settings_active = True
                    volume = open_settings(volume)  # Open the settings and update volume
        
        bg_music.set_volume(volume)
        # Draw the main menu screen
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        logo_rect = LOGO_IMAGE.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(LOGO_IMAGE, logo_rect)

        high_score_rect = HIGH_SCORE.get_rect(center=(SCREEN_WIDTH // 2, 330))
        screen.blit(HIGH_SCORE, high_score_rect)

        # Render high score text
        high_score_text = FONT.render(f"{scoreboard.high_score}", True, NAVY_BLUE)
        high_score_text_rect = high_score_text.get_rect(center=high_score_rect.center)
        screen.blit(high_score_text, high_score_text_rect)

        start_button.draw(screen)
        settings_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()