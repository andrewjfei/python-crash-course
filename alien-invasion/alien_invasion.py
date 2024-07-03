import sys
from time import sleep

import pygame

from alien import Alien
from background import Background
from bullet import Bullet
from button import Button
from game_state import GameState
from game_stats import GameStats
from game_title import GameTitle
from help import Help
from resumable_timer import ResumableTimer
from scoreboard import Scoreboard
from settings import Settings
from spaceship import Spaceship
from text import Text


def _position_button_under_existing(existing, button):
    button.rect.top = existing.rect.bottom + 25


class AlienInvasion:
    """This class is used to manage Alien Invasion assets and behaviour."""

    def __init__(self):
        pygame.init()  # initialise pygame background settings

        self.settings = Settings()

        """Uncomment below code to enable fullscreen"""
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # create pygame display window
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
            )

        # set pygame display window name
        pygame.display.set_caption(self.settings.title)

        # create a same state instance
        self.state = GameState(self)

        # create a game stats instance to track player score
        self.stats = GameStats(self)

        # create a scoreboard instance
        self.scoreboard = Scoreboard(self)

        # create help text
        self.help = Help(self)

        self.spaceship = Spaceship(self)

        # sprite group to store and manage spaceship bullets
        self.bullets = pygame.sprite.Group()

        # sprite group to store and manage aliens
        self.aliens = pygame.sprite.Group()

        # create title and button instances
        self.title = GameTitle(self)
        self.play_button = Button(self, "assets/images/play_button.bmp")
        self.help_button = Button(self, "assets/images/help_button.bmp")
        self.exit_button = Button(self, "assets/images/exit_button.bmp")
        self.resume_button = Button(self, "assets/images/resume_button.bmp")
        self.quit_button = Button(self, "assets/images/quit_button.bmp")
        self.back_button = Button(self, "assets/images/back_button.bmp")
        self.ok_button = Button(self, "assets/images/ok_button.bmp")
        self.pause_bg = Background(self, "assets/images/pause_background.bmp")

        self.pause_bg.rect.center = self.resume_button.rect.center

        # position buttons on screen correctly
        _position_button_under_existing(self.play_button, self.help_button)
        _position_button_under_existing(self.help_button, self.exit_button)
        _position_button_under_existing(self.resume_button, self.quit_button)

        # position back button
        self.back_button.rect.bottom = self.screen.get_rect().bottom - 50

        # position ok button
        self.ok_button.rect.bottom = self.screen.get_rect().bottom - 200

        # create texts used in the game
        self.game_paused_text = Text(self, "Paused", 36, (50, 50, 50))
        self.game_paused_text.text_rect.bottom = (self.resume_button.rect.top
                                                  - 40)
        self.get_ready_text = Text(self, "Get Ready...", 24)
        self.get_ready_text.text_rect.y -= 48
        self.incoming_wave_text = Text(self, "Incoming Wave...", 36)

    def run_game(self):
        while True:
            self._check_events()  # listen to keyboard and mouse events
            self._check_timer()

            if self.state.game_active and not self.state.game_over:
                self.spaceship.update()  # update spaceship position on screen

                if not self.state.get_ready and not self.state.incoming_wave:
                    self._update_bullets()
                    self._update_aliens()

            self._update_screen()  # draw elements on screen

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # exit program
            elif event.type == pygame.KEYDOWN:  # handle keydown events
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:  # handle keyup events
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button_clicked(mouse_pos)
                self._check_help_button_clicked(mouse_pos)
                self._check_exit_button_clicked(mouse_pos)
                self._check_resume_button_clicked(mouse_pos)
                self._check_quit_button_clicked(mouse_pos)
                self._check_back_button_clicked(mouse_pos)
                self._check_ok_button_clicked(mouse_pos)
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                self._check_button_hover(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.spaceship.move_right = True
        elif event.key == pygame.K_LEFT:
            self.spaceship.move_left = True
        elif event.key == pygame.K_q:
            sys.exit()  # exit program
        elif (event.key == pygame.K_SPACE and not self.state.get_ready and not
        self.state.incoming_wave):
            self._fire_bullet()
        elif event.key == pygame.K_p and self.state.game_active:
            self.state.pause_game()
            pygame.mouse.set_visible(True)  # show the mouse cursor.

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.spaceship.move_right = False
        elif event.key == pygame.K_LEFT:
            self.spaceship.move_left = False

    def _check_play_button_clicked(self, mouse_pos):
        if (not self.state.game_active and not self.state.help_active and not
        self.state.game_over):
            button_clicked = self.play_button.rect.collidepoint(mouse_pos)

            # check if the pointer of the mouse click overlaps the button
            # rectangle
            if button_clicked and not self.state.game_active:
                # reset dynamic game stat settings
                self.settings.initialise_dynamic_settings()

                self.stats.reset_stats()  # reset game stats
                self.state.start_game()

                # clear all existing bullets and aliens
                self.bullets.empty()
                self.aliens.empty()

                # create new alien fleet and center spaceship
                self._create_alien_fleet()
                self.spaceship.center_spaceship()

                # reset score
                self.scoreboard.prep_score()

                # reset level
                self.scoreboard.prep_level()

                # show lives
                self.scoreboard.prep_lives()

                pygame.mouse.set_visible(False)  # hide mouse cursor

                # Create timer to use when waiting for incoming wave of aliens.
                self.state.prepare_ready()
                self._check_get_ready_counter()

    def _check_get_ready_counter(self):
        if self.state.get_ready_counter > 0:
            self.state.get_ready_counter -= 1
            self.timer = ResumableTimer(
                1.0, self._check_get_ready_counter
                )
            self.timer.start()
        else:
            self.state.is_ready()
            self.state.reset_counter()
            self.timer = None

    def _incoming_wave(self):
        self.state.start_wave()
        self.timer = None

    def _check_timer(self):
        if hasattr(self, "timer"):
            if (self.timer is not None and self.state.game_paused and
                    self.timer.active):
                self.timer.pause()

    def _check_help_button_clicked(self, mouse_pos):
        if (not self.state.game_active and not self.state.help_active and not
        self.state.game_over):
            button_clicked = self.help_button.rect.collidepoint(mouse_pos)

            if button_clicked:
                self.state.show_help()

    def _check_exit_button_clicked(self, mouse_pos):
        if (not self.state.game_active and not self.state.help_active and not
        self.state.game_over):
            button_clicked = self.exit_button.rect.collidepoint(mouse_pos)

            # check if the pointer of the mouse click overlaps the button
            # rectangle
            if button_clicked:
                sys.exit()

    def _check_resume_button_clicked(self, mouse_pos):
        if (self.state.game_active and self.state.game_paused and not
        self.state.game_over):
            button_clicked = self.resume_button.rect.collidepoint(mouse_pos)

            if button_clicked:
                if hasattr(self, "timer"):
                    if self.timer is not None and not self.timer.active:
                        self.timer.resume()

                self.state.unpause_game()
                pygame.mouse.set_visible(False)  # hide the mouse cursor

    def _check_quit_button_clicked(self, mouse_pos):
        if (self.state.game_active and self.state.game_paused and not
        self.state.game_over):
            button_clicked = self.quit_button.rect.collidepoint(mouse_pos)

            if button_clicked:
                self.state.reset_state()

    def _check_back_button_clicked(self, mouse_pos):
        if self.state.help_active:
            button_clicked = self.back_button.rect.collidepoint(mouse_pos)

            if button_clicked:
                self.state.hide_help()  # hide help text

    def _check_ok_button_clicked(self, mouse_pos):
        if self.state.game_active and self.state.game_over:
            button_clicked = self.ok_button.rect.collidepoint(mouse_pos)

            if button_clicked:
                self.state.restart_game()

    def _check_game_inactive_buttons(self, mouse_pos):
        play_button_hover = self.play_button.rect.collidepoint(mouse_pos)
        help_button_hover = self.help_button.rect.collidepoint(mouse_pos)
        exit_button_hover = self.exit_button.rect.collidepoint(mouse_pos)
        back_button_hover = self.back_button.rect.collidepoint(mouse_pos)

        return (((play_button_hover and not self.state.help_active) or
                 (help_button_hover and not self.state.help_active) or
                 (exit_button_hover and not self.state.help_active) or
                 (back_button_hover and self.state.help_active)) and
                not self.state.game_active)

    def _check_game_active_buttons(self, mouse_pos):
        resume_button_hover = self.resume_button.rect.collidepoint(mouse_pos)
        quit_button_hover = self.quit_button.rect.collidepoint(mouse_pos)
        ok_button_hover = self.ok_button.rect.collidepoint(mouse_pos)

        return (((resume_button_hover and not self.state.game_over) or
                 (quit_button_hover and not self.state.game_over) or
                 (ok_button_hover and not self.state.game_paused and
                  self.state.game_over)) and
                self.state.game_active)

    def _check_button_hover(self, mouse_pos):

        # check if the cursor of the mouse is hovered over the button rectangle
        if (self._check_game_inactive_buttons(mouse_pos) or
                self._check_game_active_buttons(mouse_pos)):
            pygame.mouse.set_cursor(11)  # change cursor to pointer
        else:
            pygame.mouse.set_cursor(0)  # change cursor to default

    def _spaceship_hit(self):
        # set to 1 to ensure user only has 3 lives
        if self.stats.spaceships_left > 1:
            # remove a spaceship from the number of spaceships left
            self.stats.spaceships_left -= 1
            self.scoreboard.prep_lives()  # update lives on ui

            # remove all existing bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # create a new alien fleet and reset spaceship position
            self._create_alien_fleet()
            self.spaceship.center_spaceship()

            # create timer to use when waiting for incoming wave of aliens.
            self.state.prepare_ready()
            self._check_get_ready_counter()

            # pause the game for half a second
            sleep(0.5)
        else:
            self.bullets.empty()
            self.aliens.empty()
            self.state.end_game()
            pygame.mouse.set_visible(True)

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)  # add new bullet to sprite group
            self.stats.bullets_fired += 1

    def _update_bullets(self):
        self.bullets.update()  # update bullet position on screen

        # remove bullets once they have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # check if any bullets have hit any aliens
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True,
            True
            )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.stats.aliens_destroyed += 1

            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        # if all aliens have been destroyed remove existing bullets and
        # create a new alien fleet
        if not self.aliens:
            self.bullets.empty()
            self._create_alien_fleet()
            self.settings.increase_speed()

            # increase level
            self.stats.wave += 1
            self.scoreboard.prep_level()

            # pause to allow player to get ready
            self.state.prepare_wave()

            # create timer to use when waiting for incoming wave of aliens
            self.timer = ResumableTimer(1.0, self._incoming_wave)
            self.timer.start()

    def _create_alien(self, row_number, alien_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (2 * alien_width * alien_number)
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 50 + (2 * alien_height * row_number)
        self.aliens.add(alien)

    def _create_alien_fleet(self):
        alien = Alien(self)  # alien instance used to get with of alien
        alien_width, alien_height = alien.rect.size

        # determine how many aliens will fit horizontally on the screen
        available_space_x = self.settings.screen_width - (2 * alien_width)
        alien_count_x = available_space_x // (2 * alien_width)

        # determine how many rows of aliens will fit vertically on the
        # screen
        available_space_y = self.settings.screen_height - (
                6 * alien_height) - self.spaceship.rect.height
        alien_row_count = available_space_y // (2 * alien_height)

        for row_number in range(alien_row_count):
            for alien_number in range(alien_count_x):
                self._create_alien(row_number, alien_number)

    def _update_aliens(self):
        self._check_alien_fleet_screen_edges()
        self.aliens.update()  # execute update method on all alien objects

        # check if an alien has hit the spaceship
        if pygame.sprite.spritecollideany(self.spaceship, self.aliens):
            self._spaceship_hit()

        # check if any aliens have reached the bottom of the screen
        self._check_aliens_at_screen_bottom()

    def _check_alien_fleet_screen_edges(self):
        # drop alien fleet and change movement direction if any aliens reach
        # the screen edge
        for alien in self.aliens.sprites():
            if alien.check_screen_edges():
                self._change_alien_fleet_direction()
                break

    def _change_alien_fleet_direction(self):
        # drop alien fleet closer to spaceship and the ground
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        # change alien fleet movement direction
        self.settings.fleet_direction *= -1

    def _check_aliens_at_screen_bottom(self):
        screen_rect = self.screen.get_rect()

        # check if any aliens have reached the bottom of the screen
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom - 20:
                # treat this the same as if the spaceship was hit
                self._spaceship_hit()
                break

    def _update_screen(self):
        # draw background colour on screen
        self.screen.fill(self.settings.bg_colour)

        if self.state.game_active and not self.state.game_over:
            # draw spaceship on screen
            self.spaceship.blitme()

            # draw scoreboard on the screen
            self.scoreboard.show_score()

            if self.state.get_ready:
                # draw get ready text
                self.get_ready_text.draw_text()

                # create count to show on screen
                count = str(self.state.get_ready_counter + 1)
                self.counter_text = Text(self, count, 48)

                # draw count
                self.counter_text.draw_text()
            elif self.state.incoming_wave:
                # draw incoming wave text
                self.incoming_wave_text.draw_text()
            else:
                # draw all bullets on screen
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()

                # draw alien fleet on screen
                self.aliens.draw(self.screen)
        elif self.state.game_active and self.state.game_over:
            # draw game over statistics
            self.stats.show_stats()
            self.ok_button.draw_button()
        elif self.state.help_active:
            self.help.draw_help()
            self.back_button.draw_button()
        elif not self.state.game_active and not self.state.help_active:
            self.title.draw_title()
            self.play_button.draw_button()
            self.help_button.draw_button()
            self.exit_button.draw_button()

        if self.state.game_paused:
            self.pause_bg.draw_background()
            self.game_paused_text.draw_text()
            self.resume_button.draw_button()
            self.quit_button.draw_button()

        pygame.display.flip()  # show screen elements with updated positions


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
