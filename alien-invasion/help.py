import pygame.font

from data_file_finder import find_data_file


class Help:
    """This class is used to render how to play text as an image."""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # font settings for scoring information
        self.small_font = pygame.font.Font(
            find_data_file(
                "silkscreen.ttf", "fonts"
                ), 18
            )
        self.large_font = pygame.font.Font(
            find_data_file(
                "silkscreen.ttf", "fonts"
                ), 36
            )

        # Prepare help text.
        self._prep_help_title()
        self._prep_help_text()
        self._prep_how_to_title()
        self._prep_how_to_text()

    def _prep_help_title(self):
        help_title_str = "Help"
        self.help_title_image = self.large_font.render(
            help_title_str, True,
            self.settings.text_colour,
            self.settings.bg_colour
            )

        # display the title in the middle top of the screen
        self.help_title_rect = self.help_title_image.get_rect()
        self.help_title_rect.centerx = self.screen_rect.centerx
        self.help_title_rect.top = 50

    def _prep_help_text(self):
        help_text = [
            "- Press \"q\" at any time to quit the game.",
            "- Press \"p\" during the game to pause the game."]

        self.help_text_images = []
        self.help_text_rects = []

        for line in help_text:
            self.help_text_images.append(
                self.small_font.render(
                    line, True, self.settings.text_colour,
                    self.settings.bg_colour
                    )
                )

        for index in range(len(self.help_text_images)):
            # Display the help text in the middle of the screen under the title.
            self.help_text_rects.append(self.help_text_images[index].get_rect())
            self.help_text_rects[index].centerx = self.help_title_rect.centerx
            self.help_text_rects[index].top = (self.help_title_rect.bottom + 50
                                               + ((self.help_text_rects[
                                                       index].height + 20) *
                                                  index))

    def _prep_how_to_title(self):
        how_to_title_str = "How To Play"
        self.how_to_title_image = self.large_font.render(
            how_to_title_str, True,
            self.settings.text_colour,
            self.settings.bg_colour
            )

        # Display the title in the middle top of the screen.
        self.how_to_title_rect = self.how_to_title_image.get_rect()
        self.how_to_title_rect.centerx = self.screen_rect.centerx
        self.how_to_title_rect.top = self.help_text_rects[-1].bottom + 50

    def _prep_how_to_text(self):
        how_to_text = [
            "1. Use the left and right arrow keys to move the spaceship.",
            "2. Press the space key to fire a bullet.",
            "3. Only 3 bullets can be active at a time.",
            "4. If a bullet hits an alien, the alien is destroyed.",
            "5. When an entire wave is destroyed, a more advanced wave "
            "appears.",
            "6. If an alien reaches the spaceship the spaceship is destroyed.",
            "7. If an alien reaches the bottom of the screen the spaceship is "
            "destroyed",
            "8. After 3 spaceships have been destroyed the game is over.",
            "9. Destroy as many aliens as you possibly can. Good Luck!"]

        self.how_to_text_images = []
        self.how_to_text_rects = []

        for line in how_to_text:
            self.how_to_text_images.append(
                self.small_font.render(
                    line, True, self.settings.text_colour,
                    self.settings.bg_colour
                    )
                )

        for index in range(len(self.how_to_text_images)):
            # display the help text in the middle of the screen under the title
            self.how_to_text_rects.append(
                self.how_to_text_images[index].get_rect()
                )
            self.how_to_text_rects[index].centerx = (
                self.how_to_title_rect.centerx)
            self.how_to_text_rects[index].top = (
                    self.how_to_title_rect.bottom + 50 + (
                    (self.how_to_text_rects[index].height + 20) * index))

    def draw_help(self):
        self.screen.blit(self.help_title_image, self.help_title_rect)

        for index in range(len(self.help_text_images)):
            self.screen.blit(
                self.help_text_images[index],
                self.help_text_rects[index]
                )

        self.screen.blit(self.how_to_title_image, self.how_to_title_rect)

        for index in range(len(self.how_to_text_images)):
            self.screen.blit(
                self.how_to_text_images[index],
                self.how_to_text_rects[index]
                )
