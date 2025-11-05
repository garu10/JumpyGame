import pygame

from pygame.sprite import Sprite

class Enemy(Sprite):
    """A class to represent a single alien in the fleet."""
    def __init__ (self, game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # Load the ship image and scale it down
        original_image = pygame.image.load('/Users/ralphalcantara/Documents/AlienInvation_DragonBall/images/cell.bmp')

        # Define the desired size for the ship (width, height)
        new_width = original_image.get_width() // 7  # Scale to half the width
        new_height = original_image.get_height() // 7  # Scale to half the height

        # Resize the image
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        self.rect = self.image.get_rect()

        #Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move the alien right or left."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x