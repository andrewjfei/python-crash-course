import pygame
from pygame.sprite import Sprite


class SmallSpaceship(Sprite):
    """This class is used to show the players lives."""

    def __init__(self):
        super().__init__()

        # load small spaceship image
        self.image = pygame.image.load("assets/images/small_spaceship.bmp")
        self.rect = self.image.get_rect()  # store spaceship rectangle
