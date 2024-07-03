import pygame


class Spaceship:
    """This class is used to manage the spaceship entity."""

    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.state = ai_game.state
        self.screen_rect = ai_game.screen.get_rect()  # store screen rectangle

        # load spaceship image
        self.image = pygame.image.load("assets/images/spaceship.bmp")
        self.rect = self.image.get_rect()  # store spaceship rectangle

        # cast spaceship rectangle x value as a float
        self.x = float(self.rect.x)

        self.center_spaceship()  # position spaceship on screen

        # movement flags
        self.move_right = False
        self.move_left = False

    def update(self):
        if not self.state.game_paused:
            if (self.move_right and self.rect.right < self.screen_rect.right -
                    20):
                self.x += self.settings.spaceship_speed

            if self.move_left and self.rect.left > 20:
                self.x -= self.settings.spaceship_speed

            # update spaceship rectangle object
            self.rect.x = self.x

    def blitme(self):
        # draw spaceship on screen at its set location
        self.screen.blit(self.image, self.rect)

    def center_spaceship(self):
        # start spaceship at bottom center of screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.bottom -= 20

        # store spaceship's horizontal position as decimal value
        self.x = float(self.rect.x)
