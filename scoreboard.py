import pygame
import os

class Scoreboard:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.text_color = (0, 0, 128)
        self.font = pygame.font.SysFont("Black Light", 25)
        
        self.current_score = 0
        self.high_score = self._load_high_score()

    def _load_high_score(self):
        """Load the high score from a file."""
        if os.path.exists("high_score.txt"):
            with open("high_score.txt", "r") as file:
                return int(file.read())
        return 0

    def _save_high_score(self):
        """Save the high score to a file."""
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def increase_score(self, points):
        """Increase the score and update the high score if necessary."""
        self.current_score += points 
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            self._save_high_score()

    def show_score(self):
        """Render the score and high score on the screen."""
        score_str = f"Score: {self.current_score}"
        high_score_str = f"High Score: {self.high_score}"

        score_image = self.font.render(score_str, True, self.text_color)
        high_score_image = self.font.render(high_score_str, True, self.text_color)

        self.screen.blit(score_image, (20, 40))
        self.screen.blit(high_score_image, (20, 20))
