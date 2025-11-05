import pygame
import sys
import random
from game_settings import GameSettings
from player_bullets import PlayerBullet
from scoreboard import Scoreboard
from effects import Particle
from character_selection import show_characters


class JumpingGame:
    def __init__(self, volume=0.1):
        pygame.init()
        self.volume = volume

        self.bullet_sfx = pygame.mixer.Sound("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/whizzby-41134.mp3")
        #self.bullet_sfx.set_volume(volume)
        self.jumping_sfx = pygame.mixer.Sound("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/retro-jump-3-236683.mp3")
        #self.jumping_sfx.set_volume(0.1)
        self.monster_sound = pygame.mixer.Sound('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/Doodle Jump Monster Sound.mp3')
        #self.monster_sound.set_volume(volume)
        self.game_over_sfx = pygame.mixer.Sound("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/game-over-arcade-6435.mp3")
        self.ouch_sfx = pygame.mixer.Sound("/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/ow-sound-38502.mp3")

        self.set_volume(self.volume)

        # Game settings
        self.settings = GameSettings(self)
        # self.bg_color = (128, 128, 128)
        # self.black = (0, 0, 0)
        
        self.screen_width = 500
        self.screen_height = 700

        self.player_x = 100 
        self.player_y = 100

        self.platform_width = 100
        self.platform_height = 30

        #pygame.mixer.music.set_volume(self.volume)

        # Initialize screen and clock
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Jumping Jack')
        self.clock = pygame.time.Clock()

        self.bullets = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()

        self.sb = Scoreboard(self)

        # Player1 setup
        self.player1 = pygame.transform.scale(
            self.settings.jumpy_player1,
            (self.settings.player_x, self.settings.player_y)
        )
        # Player2 setup
        self.player2 = pygame.transform.scale(
            self.settings.jumpy_player2,
            (self.settings.player_x, self.settings.player_y)
        )
        # Player3 setup
        self.player3 = pygame.transform.scale(
            self.settings.jumpy_player3,
            (self.settings.player_x, self.settings.player_y)
        )
        # Player4 setup
        self.player4 = pygame.transform.scale(
            self.settings.jumpy_player4,
            (self.settings.player_x, self.settings.player_y)
        )

        self.platforms = [
                [168, 660, self.platform_width, self.platform_height, "normal"],
                [85, 570, self.platform_width, self.platform_height, "normal"],
                [265, 570, self.platform_width, self.platform_height, "super_jump"],
                [175, 470, self.platform_width, self.platform_height, "normal"],
                [85, 350, self.platform_width, self.platform_height, "normal"],
                [265, 350, self.platform_width, self.platform_height, "normal"],
                [175, 240, self.platform_width, self.platform_height, "super_jump"],
                [175, 140, self.platform_width, self.platform_height, "normal"],
                [300, 40, self.platform_width, self.platform_height, "normal"]
            ]


        self.game_blocks = []

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Spawn the first set of enemies after a delay
        self.enemy_spawn_delay = 10000  # 3 seconds after the game starts
        self.enemy_spawn_time = pygame.time.get_ticks() + self.enemy_spawn_delay  # Set spawn time
        self.enemy_visible = False  # Flag for enemy visibility

        # Bouncing variables
        self.player_speed = 3
        self.x_position_change = 0
        self.y_change = 0  # Vertical speed
        self.jump_height = 12  # Initial jump strength
        self.gravity = 0.3  # Gravity pull
        self.bounce_factor = 0.5  # Factor to reduce jump strength after each bounce
        self.on_platform = False  # Track if the player is on a platform

        self.player_rect = pygame.Rect(self.player_x + 50, self.player_y + 60, 35, 10)

        # Moving background position
        self.moving_bg_y = 0  # Initial position for the moving background

        self.shake_offset = 0  # Offset for screen shake

        # For character selection
        self.selected_character = None
        self.paused = False  # Add this line to track the paused state

    def set_volume(self, volume):
        """Set the volume for the game and its sound effects."""
        self.volume = volume
        self.monster_sound.set_volume(self.volume)
        self.bullet_sfx.set_volume(self.volume)  # Update the volume of bullet sound
        self.jumping_sfx.set_volume(self.volume)  # Update the volume of bullet sound
        self.game_over_sfx.set_volume(self.volume)
        self.ouch_sfx.set_volume(self.volume)
        print(f"Volume set to: {self.volume}")
        print("helloo")

    def run_game(self):
        """Start the main loop for the game."""
        self.selected_character = show_characters(self.screen, self.clock)
        while True:
            self._check_events()

            if not self.paused:
                # Game logic only runs when the game is not paused
                self._update_bullets()
                self._check_bullet_enemy_collision()
                self._update_screen()

                # Check if it's time to spawn the enemy
                current_time = pygame.time.get_ticks()
                if current_time >= self.enemy_spawn_time:
                    self._spawn_enemy()
                    self.enemy_spawn_time = current_time + self.enemy_spawn_delay
                    self.monster_sound.play()
                    self.monster_sound.play()

                self.clock.tick(60)
                self._player_horizontal_movement()
                self._player_bouncing()
                self._check_block_bouncingPlayer_collisions()
                self._update_platform_positions()
                self._check_player_enemy_collision()

                self.sb.show_score()
                self.set_volume(self.volume)

                self.player_rect.x = self.player_x + 40
                self.player_rect.y = self.player_y + 50

                self._update_moving_background()
            else:
                self._display_pause_screen()

    def _check_events(self):
        """Handle events such as quitting the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keyup_events(self, event):
        """Stop horizontal movement when the key is released."""
        if event.key in (pygame.K_a, pygame.K_d):  # Stop movement on release
            self.x_position_change = 0


    def _check_keydown_events(self, event):
        """Start horizontal movement when a key is pressed."""
        if event.key == pygame.K_a:  # Move left
            self.x_position_change = -self.player_speed
        elif event.key == pygame.K_d:  # Move right
            self.x_position_change = self.player_speed
        elif event.key == pygame.K_SPACE:
            self.bullet_sfx.play()
            self._fire_bullet()
        elif event.key == pygame.K_p:  # Press 'P' to pause/unpause
            self.paused = not self.paused

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:  # Limit bullets
            new_bullet = PlayerBullet(self, self.selected_character)
            self.bullets.add(new_bullet)
            
    def _display_pause_screen(self):
        """Display the pause screen while the game is paused."""
        font = pygame.font.Font(None, 74)
        text = font.render("Paused", True, (0, 0, 128))
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(text, text_rect)

        pygame.display.update()

    def _update_bullets(self):
        """Update the positions of bullets and remove off-screen bullets."""
        #Update bullet positions
        self.bullets.update()
        # Remove bullets that have gone off-screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _player_horizontal_movement(self):
        """Handle horizontal player movement."""
        acceleration = 0.5  # Adjust this value for faster/slower acceleration
        max_speed = 8  # Cap the maximum horizontal speed

        # Update speed with acceleration
        if self.x_position_change < 0:  # Moving left
            self.x_position_change = max(self.x_position_change - acceleration, -max_speed)
        elif self.x_position_change > 0:  # Moving right
            self.x_position_change = min(self.x_position_change + acceleration, max_speed)

    # Update player position
        self.player_x += self.x_position_change

    # Keep the player within screen bounds
        if self.player_x < 0:
            self.player_x = 0
            self.x_position_change = 0  # Stop movement at the boundary
        elif self.player_x > self.screen_width - 30:  # Assuming player width is 30
            self.player_x = self.screen_width - 30
            self.x_position_change = 0  # Stop movement at the boundary


    def _update_screen(self):
        """Redraw the screen and all visual elements."""
        # Draw the main static background
        if self.settings.main_bg:
            main_bg_scaled = pygame.transform.scale(self.settings.main_bg, (self.screen_width, self.screen_height))
            self.screen.blit(main_bg_scaled, (0, 0))
        else:
            self.screen.fill((0, 0, 0))  # Fallback to black background

        # Draw the moving background (with seamless scrolling)
        if self.settings.moving_bg:
            moving_bg_scaled = pygame.transform.scale(self.settings.moving_bg, (self.screen_width, self.screen_height))
            self.screen.blit(moving_bg_scaled, (0, self.moving_bg_y))
            self.screen.blit(moving_bg_scaled, (0, self.moving_bg_y - self.screen_height))
        
        if self.shake_offset > 0:
            offset_x = random.randint(-self.shake_offset, self.shake_offset)
            offset_y = random.randint(-self.shake_offset, self.shake_offset)
            self.shake_offset -= 1  # Gradually reduce the shake effect
        else:
            offset_x = 0
            offset_y = 0

        self.screen.blit(moving_bg_scaled, (offset_x, self.moving_bg_y + offset_y))

        # Draw the player character
        if self.selected_character == "Marga":
            self.screen.blit(self.player1, (self.player_x, self.player_y))
        elif self.selected_character == "Thea":
            self.screen.blit(self.player2, (self.player_x, self.player_y))
        elif self.selected_character == "Gwy":
            self.screen.blit(self.player3, (self.player_x, self.player_y))
        elif self.selected_character == "Ralph":
            self.screen.blit(self.player4, (self.player_x, self.player_y))

        self.game_blocks.clear()  # Clear old blocks before adding new ones

        # Draw platforms and align their Rects with the image
        for platform in self.platforms:
            platform_rect = pygame.Rect(platform[0], platform[1] , self.platform_width, self.platform_height)
            #pygame.draw.rect(self.screen, (0, 255, 0), platform_rect, 2)  # Green 

            if platform[4] == "super_jump":
                platform_image_scaled = pygame.transform.scale(
                    self.settings.super_platform_image, (self.platform_width, 50)
                )
                platform_rect.height = 50  # Match rect height to the scaled image
            else:
                platform_image_scaled = pygame.transform.scale(
                    self.settings.platform_image, (self.platform_width, self.platform_height)
                )

            self.screen.blit(platform_image_scaled, platform_rect.topleft)
            self.game_blocks.append(platform_rect)  # Add rect for collision detection

        # Draw all enemies
        self.enemies.update()
        self.enemies.draw(self.screen)

        self.sb.show_score()  # Draw the score

        self.all_sprites.update()  # Update all sprites (including particles)
        self.all_sprites.draw(self.screen)  # Draw all sprites


        # Draw all bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        pygame.display.update()


    def _update_moving_background(self):
        """Update the position of the moving background."""
        bg_speed = 0.5  # Adjust the speed of the scrolling
        self.moving_bg_y += bg_speed

        # Reset the background when it scrolls off-screen
        if self.moving_bg_y >= self.screen_height:
            self.moving_bg_y = 0

    
    def _update_platform_positions(self):
        screen_scroll = 0  # Initialize screen_scroll to 0
        
        if self.player_y < 450 and self.y_change < 0:
            for i in range (len(self.platforms)):
                self.platforms[i][1] -= self.y_change
            screen_scroll = self.y_change  # Track how much the screen moves
        else:
            pass
        for tiles in range (len(self.platforms)):
            if self.platforms[tiles][1] > 700:
                platform_type = "super_jump" if random.random() < 0.2 else "normal"  # 20% chance for super jump
                self.platforms[tiles] = [random.randint(10, 320), random.randint(-50, -10), 70, 10, platform_type]
                self.sb.increase_score(5)  # Increase the score by 5


                # Update enemies with the screen movement (scroll)
        self._update_enemy_positions(screen_scroll)

    def _update_enemy_positions(self, screen_scroll):
        for enemy in self.enemies:
            enemy.rect.y -= screen_scroll  # The enemies move down when the screen moves up
    
    def _spawn_enemy(self):
        """Spawn a new enemy at a random position."""
        x = random.randint(50, 350)  # Random X position within bounds
        y = random.randint(10, 15)  # Random Y position (can be adjusted)
        enemy = Enemy(x, y)
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)


    def _player_bouncing(self):
        """Handle player bouncing and falling."""
        # Apply gravity
        self.y_change += self.gravity

        # Update player's position based on y_change
        self.player_y += self.y_change

        # Check if the player falls below the screen
        if self.player_y > self.screen_height:
            print("Player fell off!")
            self._game_over_screen()  # End the game if the player falls off

    def _check_block_bouncingPlayer_collisions(self):
        """Check if the player collides with any platforms."""
        self.on_platform = False  # Reset on_platform flag

        player_rect = pygame.Rect(self.player_x + 25, self.player_y, 30, 90)  # Create a rectangle for the player
        #pygame.draw.rect(self.screen, (0, 255, 0), player_rect, 7)

        for platform in self.platforms:
            block_rect = pygame.Rect(platform[0] + 10, platform[1], platform[2] + 5, platform[3])  # Create a rectangle for each platform
            #pygame.draw.rect(self.screen, (0, 255, 0), block_rect, 7)

            if player_rect.colliderect(block_rect) and self.y_change > 0:
                # Visual effect: Highlight the platform for a brief moment
                for _ in range(20):  # Create 10 particles
                    particle = Particle(block_rect.centerx, block_rect.top)
                    self.all_sprites.add(particle)  # Add particles to a group
                self.shake_offset = 5  # Apply shake
                self.jumping_sfx.play()
                

                # Check the type of platform
                if platform[4] == "super_jump":
                    self.y_change = -self.jump_height * 1.5  # Boost jump height
                else:
                    self.y_change = -self.jump_height + 2  # Normal jump height

                self.on_platform = True  # Set on_platform to True
                break
        # self.player_y = platform[1] -10  # Adjust player_y to sit on the platform

        # If the player is not on any platform, they will continue falling
        if not self.on_platform:
            self.y_change += self.gravity
        #pygame.display.update()

            
    def _check_bullet_enemy_collision(self):
        """Check for collisions between bullets and enemies."""
        for bullet in self.bullets.sprites():
            for enemy in self.enemies.sprites():
                if bullet.rect.colliderect(enemy.rect):  # Check if bullet collides with enemy
                    self.sb.increase_score(1)  # Increase the score by 1
                    self.monster_sound.set_volume(0)
                    self.monster_sound.stop()
                    self.ouch_sfx.play()
                    bullet.kill()  # Remove the bullet
                    enemy.kill()  # Remove the enemy
                    print("Bullet hit the enemy!")
                    self.sb.current_score += 5  # Update the score display
                    break  # Break the inner loop once the collision is detected

    def _check_player_enemy_collision(self): #dipa gawa
        player_rect = pygame.Rect(self.player_x, self.player_y, 35, 10)  # Create a rectangle for the player

        for enemy in self.enemies:
            if player_rect.colliderect(enemy.rect):
                self.monster_sound.stop()
                print("Player collided with an enemy!")
                self._game_over_screen()

    def _game_over_screen(self):
        """Display the game-over screen."""
        self.game_over_sfx.play()
        self.image = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/main interface (3).png')  # Replace with the actual image path
        self.image = pygame.transform.scale(self.image, (500, 700))
        # Display the background image
        self.screen.blit(self.image, (0, 0))  # Blit the image to the top-left corner of the screen

        # Show the score below the "Game Over" text
        self.sb.show_score()

        # Wait for user input
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart the game
                        self.__init__()  # Reinitialize the game
                        self.run_game()
                    elif event.key == pygame.K_q:  # Quit the game
                        self._quit_game()

            pygame.display.update()

    def _quit_game(self):
        """Cleanly exit the game."""
        pygame.quit()
        sys.exit()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
         # Load and play monster sound
        self.image = pygame.image.load('/Users/ralphalcantara/School_Works/Second_Year/Programming/Game_Dev (Python)/JumpyGame/images_used/enemy.png')  # Replace with the actual image path
        self.image = pygame.transform.scale(self.image, (140, 90))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 5)
        # Optionally adjust the rect size here
        self.rect.width = 50  # Change the width of the rect
        self.rect.height = 90  # Change the height of the rect
        self.speed = random.choice([-3, 3])


    def update(self):
        self.rect.x += self.speed
        #reverse directuon if hitting screen bounds
        if self.rect.left <= 0 or self.rect.right >= 400:
            self.speed *= -1
        #pygame.draw.rect(self.image, (255, 0, 0), self.rect, 2)  # Draw the rect in red color


    def update_position(self, screen_scroll):
        """Move the enemy downward as the screen moves up."""
        self.rect.y += screen_scroll  # Update the vertical position of the enemy

    def remove_if_off_screen(self, screen_height):
        """Remove the enemy if it moves off-screen."""
        if self.rect.top > screen_height:
            self.kill()  # Remove the enemy from all groups

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        self.rect.x = self.player_x
        self.rect.y = self.player_y


if __name__ == '__main__':
    game = JumpingGame()
    game.run_game()
