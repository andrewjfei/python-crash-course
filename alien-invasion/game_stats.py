import pygame

from data_file_finder import find_data_file


class GameStats:
    """This class is used to track the statistics for Alien Invasion."""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        self.spaceships_left = None
        self.score = None
        self.high_score = 0
        self.wave = None
        self.bullets_fired = None
        self.aliens_destroyed = None

        self.reset_stats()

        # font settings for scoring information
        self.small_font = pygame.font.Font(
            find_data_file(
                "silkscreen.ttf",
                "fonts"
                ), 24
            )
        self.large_font = pygame.font.Font(
            find_data_file(
                "silkscreen.ttf",
                "fonts"
                ), 48
            )

        # open high score file and create file if it does not exist
        with open(self.settings.high_score_filename, "a+") as file:
            file.seek(0)
            high_score_str = file.read()

            if high_score_str:
                self.high_score = int(high_score_str)

    def reset_stats(self):
        self.spaceships_left = self.settings.spaceship_limit
        self.score = 0
        self.wave = 1
        self.aliens_destroyed = 0
        self.bullets_fired = 0

    def _prep_stats(self):
        self._prep_game_over_text()
        self._prep_bullets_fired()
        self._prep_aliens_destroyed()
        self._prep_accuracy()
        self._prep_wave()
        self._prep_score()

    def _prep_game_over_text(self):
        game_over_title_str = "Game Over!"
        self.game_over_title_image = self.large_font.render(
            game_over_title_str, True, self.settings.text_colour,
            self.settings.bg_colour
            )

        # display the title in the middle top of the screen
        self.game_over_title_rect = self.game_over_title_image.get_rect()
        self.game_over_title_rect.centerx = self.screen_rect.centerx
        self.game_over_title_rect.top = 200

    def _prep_bullets_fired(self):
        bullets_fired_str = f"Bullets Fired: {self.bullets_fired}"
        self.bullets_fired_image = self.small_font.render(
            bullets_fired_str, True, self.settings.text_colour,
            self.settings.bg_colour
            )

        # display the bullets fired under the title
        self.bullets_fired_rect = self.bullets_fired_image.get_rect()
        self.bullets_fired_rect.centerx = self.screen_rect.centerx
        self.bullets_fired_rect.top = self.game_over_title_rect.bottom + 50

    def _prep_aliens_destroyed(self):
        aliens_destroyed_str = f"Aliens Destroyed: {self.aliens_destroyed}"
        self.aliens_destroyed_image = self.small_font.render(
            aliens_destroyed_str, True, self.settings.text_colour,
            self.settings.bg_colour
            )

        # display the number aliens destroyed under the title
        self.aliens_destroyed_rect = self.aliens_destroyed_image.get_rect()
        self.aliens_destroyed_rect.centerx = self.screen_rect.centerx
        self.aliens_destroyed_rect.top = self.bullets_fired_rect.bottom + 20

    def _prep_accuracy(self):
        if self.bullets_fired != 0:
            accuracy = int((self.aliens_destroyed / self.bullets_fired) * 100)
        else:
            accuracy = 0
        accuracy_str = f"Accuracy: {accuracy}%"
        self.accuracy_image = self.small_font.render(
            accuracy_str, True, self.settings.text_colour,
            self.settings.bg_colour
            )

        # Display the number aliens destroyed under the title.
        self.accuracy_rect = self.accuracy_image.get_rect()
        self.accuracy_rect.centerx = self.screen_rect.centerx
        self.accuracy_rect.top = self.aliens_destroyed_rect.bottom + 20

    def _prep_wave(self):
        wave_str = f"Wave Reached: {self.wave}"
        self.wave_image = self.small_font.render(
            wave_str, True,
            self.settings.text_colour, self.settings.bg_colour
            )

        # Display the wave reached under the title.
        self.wave_rect = self.wave_image.get_rect()
        self.wave_rect.centerx = self.screen_rect.centerx
        self.wave_rect.top = self.accuracy_rect.bottom + 20

    def _prep_score(self):
        score_str = f"Score: {self.score}"
        self.score_image = self.small_font.render(
            score_str, True,
            self.settings.text_colour, self.settings.bg_colour
            )

        # Display the wave reached under the title.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centerx = self.screen_rect.centerx
        self.score_rect.top = self.wave_rect.bottom + 20

    def show_stats(self):
        # prepare stats to draw onto screen
        self._prep_stats()

        self.screen.blit(self.game_over_title_image, self.game_over_title_rect)
        self.screen.blit(self.bullets_fired_image, self.bullets_fired_rect)
        self.screen.blit(
            self.aliens_destroyed_image,
            self.aliens_destroyed_rect
            )
        self.screen.blit(self.accuracy_image, self.accuracy_rect)
        self.screen.blit(self.wave_image, self.wave_rect)
        self.screen.blit(self.score_image, self.score_rect)
