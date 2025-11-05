import pygame
import sys

# Define constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
BLUE = (0, 0, 225)
character_image_x = 100
character_image_y = 200
# Initialize the mixer (to handle sounds)
pygame.mixer.init()

# Load images
BACKGROUND_IMAGE = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/bgmain.png")
CHARACTER_IMAGE1 = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/7.png")
CHARACTER_IMAGE2 = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/8.png")
CHARACTER_IMAGE3 = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/9.png")
CHARACTER_IMAGE4 = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/10.png")
ARROW_LEFT = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/12.png")
ARROW_RIGHT = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/13.png")
SELECT_BUTTON = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/11.png")
HOME_BUTTON = pygame.image.load("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/6.png")
select_sfx = pygame.mixer.Sound("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/menu-button-89141.mp3")
selectbutton_sfx = pygame.mixer.Sound("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/menu-button-88360.mp3")

# Scale images
CHARACTER_IMAGE1 = pygame.transform.scale(CHARACTER_IMAGE1, (400, 300))
CHARACTER_IMAGE2 = pygame.transform.scale(CHARACTER_IMAGE2, (400, 300))
CHARACTER_IMAGE3 = pygame.transform.scale(CHARACTER_IMAGE3, (400, 300))
CHARACTER_IMAGE4 = pygame.transform.scale(CHARACTER_IMAGE4, (400, 300))
ARROW_LEFT = pygame.transform.scale(ARROW_LEFT, (500, 500))
ARROW_RIGHT = pygame.transform.scale(ARROW_RIGHT, (500, 500))
SELECT_BUTTON = pygame.transform.scale(SELECT_BUTTON, (150, 200))
HOME_BUTTON = pygame.transform.scale(HOME_BUTTON, (500, 500))

class Button:
    def __init__(self, image, x, y, width, height, action=None):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.action = action

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            if callable(self.action):
                self.action()
            elif self.action == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

def show_characters(screen, clock):
    # Initialize FONT inside the function after Pygame is initialized
    FONT = pygame.font.Font(None, 36)

    characters_running = True
    character_images = [CHARACTER_IMAGE1, CHARACTER_IMAGE2, CHARACTER_IMAGE3, CHARACTER_IMAGE4]
    character_names = ["Marga", "Thea", "Gwy", "Ralph"]
    current_index = 0
    selected_character = None

    arrow_left_button = Button(ARROW_LEFT, SCREEN_WIDTH // 3 - 200, SCREEN_HEIGHT // 6 - 25, 350, 300)
    arrow_right_button = Button(ARROW_RIGHT, SCREEN_WIDTH // 8 + 150, SCREEN_HEIGHT // 6 - 25, 350, 300)
    select_button = Button(SELECT_BUTTON, SCREEN_WIDTH // 3 - 115, SCREEN_HEIGHT - 240, 400, 150)

    while characters_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if arrow_left_button.rect.collidepoint(mouse_pos):
                    current_index = (current_index - 1) % len(character_images)
                    select_sfx.play()
                elif arrow_right_button.rect.collidepoint(mouse_pos):
                    current_index = (current_index + 1) % len(character_images)
                    select_sfx.play()
                elif select_button.rect.collidepoint(mouse_pos):
                    selected_character = character_names[current_index]
                    selectbutton_sfx.play()
                    characters_running = False

        screen.blit(BACKGROUND_IMAGE, (0, 0))

        current_character = character_images[current_index]
        current_character_rect = current_character.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(current_character, current_character_rect)

        character_name_text = FONT.render(character_names[current_index], True, BLUE)
        screen.blit(character_name_text, (SCREEN_WIDTH // 2 - character_name_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

        arrow_left_button.draw(screen)
        arrow_right_button.draw(screen)
        select_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    return selected_character
