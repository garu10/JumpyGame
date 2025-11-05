import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.life = random.randint(20, 40)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-3, -1)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.life -= 1
        if self.life <= 0:
            self.kill()  # Remove the particle after its life ends
            
class ParticleSystem:
    def __init__(self, x, y):
        self.particles = []
        self.x = x
        self.y = y

    def emit(self):
        # Emit new particles
        for _ in range(5):  # Number of particles per frame
            self.particles.append(
                Particle(
                    self.x + random.randint(-10, 10),  # Random offset
                    self.y + random.randint(-10, 10),
                    (255, 50, 50),  # Red color
                    random.randint(30, 50),  # Lifespan
                    random.randint(3, 6)  # Size
                )
            )

    def update(self):
        # Update all particles
        for particle in self.particles[:]:
            particle.update()
            if particle.lifespan <= 0:
                self.particles.remove(particle)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)
