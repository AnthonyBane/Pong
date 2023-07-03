"""This module contains the classes and functionality to run a basic version of the Pong video game 
   """
__version__ = "3.0"

# TODO - refactor constants to use config file or revert to defaults

import pygame
from logger_setup import logger
from paddle import Paddle
from ball import Ball
from player import Player

# Defining window size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# Defining colour tuples in RGB
# TODO - refactor colours to ENUM
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game limiting FPS
FPS_LIMIT = 60

# Paddle size
PADDLE_HEIGHT = 100
PADDLE_WIDTH = 20

# Score to reach
MAX_SCORE = 5

# Game window and name
GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong")
logger.info("Window set to width: %s, and height: %s", WINDOW_WIDTH, WINDOW_HEIGHT)


class Pong:
    """Pong game class handling game flow and logic"""

    def __init__(self, player_one_name: str = "Player 1", player_two_name: str = "Player 2") -> None:
        """Pong game class init.

        Args:
            player_one_name (str, optional): Player one's name. Defaults to "Player 1".
            player_two_name (str, optional): Player two's name. Defaults to "Player 2".
        """
        logger.info("Initializing Pong game.")
        pygame.init()
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.SysFont("Britannic", 50)

        self.paddle_left = Paddle(
            x_position=10,
            y_position=WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2,
            width=PADDLE_WIDTH,
            height=PADDLE_HEIGHT,
            colour=WHITE,
        )
        self.paddle_right = Paddle(
            x_position=WINDOW_WIDTH - PADDLE_WIDTH - 10,
            y_position=WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2,
            width=PADDLE_WIDTH,
            height=PADDLE_HEIGHT,
            colour=WHITE,
        )
        self.ball = Ball(
            x_position=WINDOW_WIDTH // 2,
            y_position=WINDOW_HEIGHT // 2,
            radius=5,
            x_velocity=5,
            y_velocity=0,
            colour=WHITE,
        )

        self.player_one = Player(player_one_name, 0)
        self.player_two = Player(player_two_name, 0)

    def move_paddle(self, keys):
        """Handles paddle movement

        Args:
            keys (pygame.key.ScancodeWrapper): A list of key presses.
        """

        if keys[pygame.K_w] and self.paddle_left.y_position >= 0:
            self.paddle_left.y_position -= 5
        if keys[pygame.K_s] and self.paddle_left.y_position <= WINDOW_HEIGHT - self.paddle_left.height:
            self.paddle_left.y_position += 5

        if keys[pygame.K_UP] and self.paddle_right.y_position >= 0:
            self.paddle_right.y_position -= 5
        if keys[pygame.K_DOWN] and self.paddle_right.y_position <= WINDOW_HEIGHT - self.paddle_right.height:
            self.paddle_right.y_position += 5

    def move_ball(self):
        """Handles changes in ball velocity"""
        self.ball.x_position += self.ball.x_velocity
        self.ball.y_position += self.ball.y_velocity

    # TODO - add docstring
    def get_paddles(self):
        return [self.paddle_left, self.paddle_right]

    # TODO - add docstring
    def get_ball(self):
        return self.ball

    def calculate_return_y_velocity(self, paddle: Paddle, ball: Ball) -> int:
        """Helper function to calculate y velocity after paddle collision

        Args:
            paddle (Paddle): paddle the ball hit
            ball (Ball): the ball

        Returns:
            int: calculated y velocity
        """
        displacement_from_paddle = ball.y_position - (paddle.y_position + (paddle.height // 2))
        reduction = (paddle.height // 2) / ball.max_velocity
        y_velocity = displacement_from_paddle / reduction
        return y_velocity

    # TODO - change to handle ball collision or separate paddle and ceiling collisions.
    # TODO - refactor so that ball and paddle collisions happen at paddle borders instead of before/after paddle edges
    def handle_paddle_collision(self):
        """Handles ball collisions."""
        if self.ball.y_position <= 0 + self.ball.radius or self.ball.y_position >= WINDOW_HEIGHT - self.ball.radius:
            self.ball.y_velocity *= -1

        if (
            self.ball.y_position >= self.paddle_left.y_position
            and self.ball.y_position <= self.paddle_left.y_position + self.paddle_left.height
        ):
            if self.ball.x_position - self.ball.radius <= self.paddle_left.x_position + self.paddle_left.width:
                self.ball.x_velocity *= -1
                self.ball.y_velocity = self.calculate_return_y_velocity(self.paddle_left, self.ball)

        if (
            self.ball.y_position >= self.paddle_right.y_position
            and self.ball.y_position <= self.paddle_right.y_position + self.paddle_right.height
        ):
            if self.ball.x_position + self.ball.radius >= self.paddle_right.x_position:
                self.ball.x_velocity *= -1
                self.ball.y_velocity = self.calculate_return_y_velocity(self.paddle_right, self.ball)

    def draw(self, window):
        """Handles the drawing of visual elements to the game window

        Args:
            window (pygame.display): The Pong game window.
        """

        # Reset canvas
        window.fill(BLACK)

        # Draw the paddles
        pygame.draw.rect(
            window,
            self.paddle_left.colour,
            (
                self.paddle_left.x_position,
                self.paddle_left.y_position,
                self.paddle_left.width,
                self.paddle_left.height,
            ),
        )
        pygame.draw.rect(
            window,
            self.paddle_right.colour,
            (
                self.paddle_right.x_position,
                self.paddle_right.y_position,
                self.paddle_right.width,
                self.paddle_right.height,
            ),
        )

        # Draws the scores
        score_one_text = self.game_font.render(f"{self.player_one.score}", 1, WHITE)
        score_two_text = self.game_font.render(f"{self.player_two.score}", 1, WHITE)
        window.blit(score_one_text, (WINDOW_WIDTH // 4 - score_one_text.get_width() // 2, 20))
        window.blit(
            score_two_text,
            (WINDOW_WIDTH * (3 / 4) - score_two_text.get_width() // 2, 20),
        )

        # Draw the ball
        pygame.draw.circle(
            window,
            self.ball.colour,
            (self.ball.x_position, self.ball.y_position),
            self.ball.radius,
        )

        # Detect if there is a winner
        # TODO - refactor this to send winner a player name
        if self.player_one.score >= MAX_SCORE or self.player_two.score >= MAX_SCORE:
            self.winner(window)
        else:
            pygame.display.update()

    # TODO - refactor winner() - to take a name
    def winner(self, window):
        """Handles writing to the window and resetting the game if a winner is identified.

        Args:
            window (pygame.display): The Pong game window.
        """
        if self.player_one.score >= MAX_SCORE:
            winning_text = f"{self.player_one.name} has won!"
            logger.info("Player: %s, has own the game.", self.player_one.name)
        elif self.player_two.score >= MAX_SCORE:
            winning_text = f"{self.player_two.name} has won!"
            logger.info("Player: %s, has own the game.", self.player_two.name)

        text_to_write = self.game_font.render(winning_text, 1, WHITE)
        window.fill(BLACK)
        window.blit(
            text_to_write,
            (
                WINDOW_WIDTH // 2 - text_to_write.get_width() // 2,
                WINDOW_HEIGHT // 2 - text_to_write.get_height() // 2,
            ),
        )
        logger.info("Resetting player scores.")
        self.player_one.score = 0
        self.player_two.score = 0
        pygame.display.update()
        pygame.time.delay(5000)

    def reset(self):
        """Resets the paddle and ball positions as well as ball y_velocity. Ball x_velocity is not impacted."""
        logger.info("Resetting ball and paddles to original positions.")
        self.ball.x_position = self.ball.x_position_original
        self.ball.y_position = self.ball.y_position_original
        self.ball.y_velocity = 0

        self.paddle_left.y_position = self.paddle_left.y_position_original

        self.paddle_right.y_position = self.paddle_right.y_position_original

    def goal(self):
        """Handles a goal outcome"""
        if self.ball.x_position < 0:
            self.player_two.score += 1
            logger.info("Player: %s, has scored. Total score is now: %s", self.player_two.name, self.player_two.score)
            self.reset()

        elif self.ball.x_position > WINDOW_WIDTH:
            self.player_one.score += 1
            logger.info("Player: %s, has scored. Total score is now: %s", self.player_one.name, self.player_one.score)
            self.reset()

    def run_game(self):
        """Contains the game loop. Handles window closure."""
        run = True
        logger.info("Setting the game loop controller run to: %s", run)

        while run:
            self.clock.tick(FPS_LIMIT)
            self.draw(GAME_WINDOW)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    logger.info("Game encountered pygame.QUIT signal, game closing.")
                    break

            keys = pygame.key.get_pressed()
            self.move_paddle(keys)
            self.move_ball()
            self.handle_paddle_collision()
            self.goal()

        pygame.quit()


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description='Welcome to the Pong game. This is an example of a script "help" command that could be fleshed out further.',
        epilog="This is the end of the help section.",
    )
    parser.add_argument("-d", "--debug", help="Runs the program in debug mode.", action="store_true")
    args, unknown = parser.parse_known_args()
    if args.debug:
        import logging

        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug('Received "--debug" command, running the program in debug mode.')
    if unknown:
        for arg in unknown:
            logger.info("Unhandled argument %s", arg)


def main():
    """The entry point to the program"""
    parse_args()
    game = Pong()
    game.run_game()


if __name__ == "__main__":
    main()
