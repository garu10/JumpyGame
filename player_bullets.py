import pygame

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, game, character):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings


        # Assign a different bullet image based on the character
        if character == "Marga":
            self.image = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/17.png')  # Replace with the actual image path
            self.image = pygame.transform.scale(self.image, (100, 60))  # Resize bullet
        elif character == "Thea":
            self.image = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/21.png')  # Replace with the actual image path
            self.image = pygame.transform.scale(self.image, (100, 60))  # Resize bullet
        elif character == "Gwy":
            self.image = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/20.png')  # Replace with the actual image path
            self.image = pygame.transform.scale(self.image, (100, 60))  # Resize bullet
        elif character == "Ralph":
            self.image = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/16.png')  # Replace with the actual image path
            self.image = pygame.transform.scale(self.image, (100, 60))  # Resize bullet
        else:
            self.image = pygame.Surface((10, 5))
            self.image.fill((255, 255, 255))  # Default bullet

        self.rect = self.image.get_rect()
        self.rect.centerx = game.player_x + 40  # Center bullet horizontally with player
        self.rect.top = game.player_y  # Position bullet at the player's top

        self.speed = 10  # Adjust bullet speed as needed

    def update(self):
        """Move the bullet upward."""
        self.rect.y -= self.speed  # Move bullet upwards
        if self.rect.bottom <= 0:
            self.kill()  # Remove the bullet when it goes off-screen

    def draw_bullet(self):
        """Draw the bullet image to the screen."""
        self.screen.blit(self.image, self.rect)
