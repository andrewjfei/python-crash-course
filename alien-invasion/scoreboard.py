import pygame.sysfont
from pygame.sprite import Group

from data_file_finder import find_data_file
from small_spaceship import SmallSpaceship


class Scoreboard:
    """This class is used to report scoring information in Alien Invasion."""

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.spaceship_lives = None

        self.score_image = None
        self.score_rect = None

        self.high_score_image = None
        self.high_score_rect = None

        self.level_image = None
        self.level_rect = None

        # font settings for scoreboard
        self.small_font = pygame.font.Font(
            find_data_file(
                "silkscreen.ttf", "fonts"
                ), 16
            )
        self.medium_font = pygame.font.Font(
            find_data_file(
                "silkscreen.ttf", "fonts"
                ), 24
            )
        self.large_font = pygame.font.Font(
            find_data_file(
                "silkscreen.ttf", "fonts"
                ), 36
            )

        # prepare score images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives()

    def prep_score(self):
        # round score to the nearest 10
        rounded_score = round(self.stats.score, -1)

        # format string with commas for large numbers
        score_str = "{:,}".format(rounded_score)

        self.score_image = self.medium_font.render(
            score_str, True,
            self.settings.text_colour,
            self.settings.bg_colour
            )

        self.score_rect = self.score_image.get_rect()

        # set scoreboard position on screen
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)

        self.high_score_image = self.large_font.render(
            high_score_str, True,
            self.settings.text_colour,
            self.settings.bg_colour
            )

        self.high_score_rect = self.high_score_image.get_rect()

        # center high score at the top of the screen
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            # write new high score to file
            with open(self.settings.high_score_filename, "w") as file:
                file.write(str(self.stats.score))

            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        level_str = f"Wave {str(self.stats.wave)}"

        self.level_image = self.small_font.render(
            level_str, True,
            self.settings.text_colour,
            self.settings.bg_colour
            )

        self.level_rect = self.level_image.get_rect()

        # set level position under the score
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_lives(self):
        self.spaceship_lives = Group()

        for spaceship_number in range(self.stats.spaceships_left):
            spaceship = SmallSpaceship()
            spaceship.rect.left = 20 + (
                    (spaceship_number * spaceship.rect.width) + (
                    spaceship_number * 10))
            spaceship.rect.top = 20
            self.spaceship_lives.add(spaceship)

    def show_score(self):
        # draw scoreboard, high score and level on the screen
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.spaceship_lives.draw(self.screen)
