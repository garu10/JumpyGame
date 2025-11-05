import pygame


class GameSettings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self, game):
        """Initialize the game's static and dynamic settings."""

        # Main static background
        self.main_bg = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/main_bg.png')
        self.main_bg2 = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/mainbg2.png')
        
        # Moving background
        self.moving_bg = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/moving_bg.png')


        # Screen settings
        # self.screen_width = 400
        # self.screen_height = 500
        self.bg_color = (0,0, 0)

        self.jumpy_player1 = self.jumpy_player = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/7.png')
        self.jumpy_player2 = self.jumpy_player = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/8.png')
        self.jumpy_player3 = self.jumpy_player = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/9.png')
        self.jumpy_player4 = self.jumpy_player = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/10.png')

        self.enemy_player = self.jumpy_enemy = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/cell.bmp')
        
        self.platform_image = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/platformm.png')
        self.super_platform_image = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/super_platform.png')


        self.player_x = 170 // 2
        self.player_y = 150 // 2
        # self.player_pos_x = game.width // 2 - self.player_x // 2  # Center horizontally
        # self.player_pos_y = game.height - self.player_y - 10  # Near the bottom

        self.enemy_x = 50
        self.enemy_y = 50

        self.enemy_width = 10  # Enemy width
        self.enemy_height = 10  # Enemy height


        # Bullet settings
        self.bullet_width = 10
        self.bullet_height = 10
        self.bullet_color = (0, 191, 255)  # Light blue bullets
        self.bullets_allowed = 5