import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """This class is used to manage the bullets from the spaceship."""

    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.state = ai_game.state
        self.colour = self.settings.bullet_colour

        # create bullet rectangle
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width,
            self.settings.bullet_height
            )

        # set initial position of bullet
        self.rect.midtop = ai_game.spaceship.rect.midtop

        # store bullet's vertical position as decimal value
        self.y = float(self.rect.y)

    def update(self):
        if not self.state.game_paused:
            self.y -= self.settings.bullet_speed

            # update bullet rectangle object
            self.rect.y = self.y

    def draw_bullet(self):
        # draw bullet on screen
        pygame.draw.rect(self.screen, self.colour, self.rect)
