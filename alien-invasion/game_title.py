import pygame.font

from data_file_finder import find_data_file


class GameTitle:
    """This class is used to render the game title."""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.title = self.settings.title

        self.font = pygame.font.Font(find_data_file(
            "silkscreen.ttf", "fonts"), 60)

        self.title_image = self.font.render(self.title, True,
                                            self.settings.text_colour,
                                            self.settings.bg_colour)

        # display the title at the top middle of the screen
        self.title_rect = self.title_image.get_rect()
        self.title_rect.centerx = self.screen_rect.centerx
        self.title_rect.top = 200

    def draw_title(self):
        self.screen.blit(self.title_image, self.title_rect)
