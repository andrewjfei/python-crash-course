import pygame.image
from pygame.sprite import Sprite


class Alien(Sprite):
    """This class is used to represent a single alien within the fleet."""

    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.state = ai_game.state

        # load alien image
        self.image = pygame.image.load("assets/images/alien.bmp")
        self.rect = self.image.get_rect()  # store alien rectangle

        # set alien position on screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store alien's horizontal position as decimal value
        self.x = float(self.rect.x)

    def update(self):
        if not self.state.game_paused:
            self.x += self.settings.alien_speed * self.settings.fleet_direction

            # update alien rectangle object
            self.rect.x = self.x

    """Return True if an alien is at the edge of the screen."""

    def check_screen_edges(self):
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right - 20 or self.rect.left <= 20:
            return True
