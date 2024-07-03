class Settings:
    """This class is used to store all settings for Alien Invasion."""

    def __init__(self):
        self.title = "Alien Invasion"
        self.high_score_filename = "high_score.txt"
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (30, 30, 30)  # store background colour
        self.text_colour = (230, 230, 230)

        self.get_ready_counter = 3

        # spaceship settings
        self.spaceship_speed = None
        self.spaceship_limit = 3

        # bullet settings
        self.bullet_speed = None
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_colour = (255, 165, 0)
        self.bullets_allowed = 3

        # alien settings
        self.alien_speed = None
        self.alien_points = None
        self.fleet_drop_speed = 10
        self.fleet_direction = None

        # how quickly the game speeds up
        self.speedup_scale = 1.1

        # how quickly the alien points increase
        self.score_scale = 1.5

        self.initialise_dynamic_settings()

    def initialise_dynamic_settings(self):
        # dynamic spaceship settings
        self.spaceship_speed = 1.5

        # dynamic bullet settings
        self.bullet_speed = 3.0

        # dynamic alien settings
        self.alien_speed = 0.5
        self.alien_points = 50
        self.fleet_direction = 1  # 1 represents right and -1 represents left

    def increase_speed(self):
        self.spaceship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
