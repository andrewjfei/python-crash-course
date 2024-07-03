import pygame.font

from data_file_finder import find_data_file


class Text:
    """This class is used to display text on the screen."""

    def __init__(self, ai_game, text, size, bg_colour=None):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        self.font = pygame.font.Font(
            find_data_file(
                "silkscreen.ttf", "fonts"
                ), size
            )

        self.text_image = self.font.render(
            text, True,
            self.settings.text_colour,
            self.settings.bg_colour if bg_colour is None else bg_colour
            )

        # Display the text in the middle of the screen.
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = self.screen_rect.center

    def draw_text(self):
        self.screen.blit(self.text_image, self.text_rect)
