class GameState:
    """This class is used to capture the state of Alien Invasion."""

    def __init__(self, ai_game):
        self.settings = ai_game.settings

        self.game_active = None
        self.game_paused = None
        self.help_active = None
        self.game_over = None
        self.get_ready = None
        self.incoming_wave = None
        self.get_ready_counter = None

        self.reset_state()

    def start_game(self):
        self.game_active = True

    def end_game(self):
        self.game_over = True

    def restart_game(self):
        self.game_active = False
        self.game_over = False

    def pause_game(self):
        self.game_paused = True

    def unpause_game(self):
        self.game_paused = False

    def show_help(self):
        self.help_active = True

    def hide_help(self):
        self.help_active = False

    def prepare_ready(self):
        self.get_ready = True

    def is_ready(self):
        self.get_ready = False

    def prepare_wave(self):
        self.incoming_wave = True

    def start_wave(self):
        self.incoming_wave = False

    def reset_counter(self):
        self.get_ready_counter = self.settings.get_ready_counter

    def reset_state(self):
        self.game_active = False
        self.game_paused = False
        self.help_active = False
        self.game_over = False
        self.get_ready = False
        self.incoming_wave = False
        self.reset_counter()
