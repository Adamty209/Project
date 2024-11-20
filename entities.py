# entities.py
import pygame

# Define the Player class
class Player:
    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 0.5
        self.rect = pygame.Rect(self.x, self.y, 50, 50)  # Represent player as a rectangle for now
        self.velocity_x = 0
        self.velocity_y = 0
        self.sprite = None
        if self.sprite:
            self.sprite = pygame.transform.scale(self.sprite, (75, 75))  # Scale sprite to be larger

    def move(self, keys):
        acceleration = 0.04
        deceleration = 0.03
        max_speed = 0.2

        # Handle acceleration
        if keys[pygame.K_LEFT]:
            self.velocity_x = max(self.velocity_x - acceleration, -max_speed)
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = min(self.velocity_x + acceleration, max_speed)
        else:
            # Decelerate to stop
            if self.velocity_x > 0:
                self.velocity_x = max(self.velocity_x - deceleration, 0)
            elif self.velocity_x < 0:
                self.velocity_x = min(self.velocity_x + deceleration, 0)

        if keys[pygame.K_UP]:
            self.velocity_y = max(self.velocity_y - acceleration, -max_speed)
        elif keys[pygame.K_DOWN]:
            self.velocity_y = min(self.velocity_y + acceleration, max_speed)
        else:
            # Decelerate to stop
            if self.velocity_y > 0:
                self.velocity_y = max(self.velocity_y - deceleration, 0)
            elif self.velocity_y < 0:
                self.velocity_y = min(self.velocity_y + deceleration, 0)

        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Boundary checks
        self.x = max(0, min(self.x, self.screen_width - self.rect.width))
        self.y = max(0, min(self.y, self.screen_height - self.rect.height))

        # Update player rectangle position
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        if self.sprite:
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, (0, 255, 0), self.rect)

# Define the NPC class
class NPC:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 50, 50)  # Represent NPC as a rectangle for now
        self.dialogue = "Hello, traveler!"
        self.sprite = None

    def draw(self, screen):
        if self.sprite:
            screen.blit(self.sprite, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
