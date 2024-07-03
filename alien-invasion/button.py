import pygame.sysfont


class Button:
    """This class is used represent a button."""

    def __init__(self, ai_game, image_path):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # load button image
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()  # store button rectangle
        self.rect.center = self.screen_rect.center

    def draw_button(self):
        self.screen.blit(self.image, self.rect)
