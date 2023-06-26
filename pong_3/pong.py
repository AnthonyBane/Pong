"""This module contains the classes and functionality to run a basic version of the Pong video game 
   """
__version__ = "2.0"

import pygame
from dataclasses import dataclass

# Defining window size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# Defining colour tuples in RGB
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


class Paddle:
    """Paddle class used to create paddles for the pong game."""

    def __init__(
        self, x_position, y_position, width, height, colour=WHITE, paddle_velocity=4
    ) -> None:
        """Paddle class init.

        Args:
            x_position (int): current x position
            y_position (int): current y position
            width (int): width in pixels
            height (int): height in pixels
            colour (tuple, optional): paddle fill colour
            paddle_velocity (int, optional): paddle velocity. Defaults to 4.
        """
        self.x_position = x_position
        self.y_position = self.y_position_original = y_position
        self.width = width
        self.height = height
        self.colour = colour
        self.paddle_velocity = paddle_velocity

    def move(self, up=True):
        """Changes the paddle's xy positions.

        Args:
            up (bool): Signals whether to add or remove the y velocity. Defaults to True.
        """
        if up:
            self.y_position += self.paddle_velocity
        else:
            self.y_position -= self.paddle_velocity


class Ball:
    """Ball class used to create a ball for the ball game."""

    def __init__(
        self,
        x_position: int,
        y_position: int,
        radius: int,
        x_velocity: int = 5,
        y_velocity: int = 0,
        colour: tuple = WHITE,
        max_velocity: int = 5,
    ) -> None:
        """Ball class init.

        Args:
            x_position (int): current x position.
            y_position (int): current y position.
            radius (int): ball radius in pixels.
            x_velocity (int, optional): x velocity. Defaults to 5.
            y_velocity (int, optional): y velocity. Defaults to 0.
            colour (tuple, optional): ball colour fill. Defaults to WHITE.
            max_velocity (int, optional): max potential velocity. Defaults to 5.
        """
        self.x_position = self.x_position_original = x_position
        self.y_position = self.y_position_original = y_position
        self.radius = radius
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.max_velocity = max_velocity
        self.colour = colour


@dataclass
class Player:
    """Example Player class"""

    name: str
    score: int = 0


class Pong:
    """Pong game class handling game flow and logic"""

    def __init__(
        self, player_one_name: str = "Player 1", player_two_name: str = "Player 2"
    ) -> None:
        """Pong game class init.

        Args:
            player_one_name (str, optional): Player one's name. Defaults to "Player 1".
            player_two_name (str, optional): Player two's name. Defaults to "Player 2".
        """
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
        if (
            keys[pygame.K_s]
            and self.paddle_left.y_position <= WINDOW_HEIGHT - self.paddle_left.height
        ):
            self.paddle_left.y_position += 5

        if keys[pygame.K_UP] and self.paddle_right.y_position >= 0:
            self.paddle_right.y_position -= 5
        if (
            keys[pygame.K_DOWN]
            and self.paddle_right.y_position <= WINDOW_HEIGHT - self.paddle_right.height
        ):
            self.paddle_right.y_position += 5

    def move_ball(self):
        """Handles changes in ball velocity"""
        self.ball.x_position += self.ball.x_velocity
        self.ball.y_position += self.ball.y_velocity

    def get_paddles(self):
        return [self.paddle_left, self.paddle_right]

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

    def handle_paddle_collision(self):
        """Handles ball collisions."""
        if (
            self.ball.y_position <= 0 + self.ball.radius
            or self.ball.y_position >= WINDOW_HEIGHT - self.ball.radius
        ):
            self.ball.y_velocity *= -1

        if (
            self.ball.y_position >= self.paddle_left.y_position
            and self.ball.y_position <= self.paddle_left.y_position + self.paddle_left.height
        ):
            if (
                self.ball.x_position - self.ball.radius
                <= self.paddle_left.x_position + self.paddle_left.width
            ):
                self.ball.x_velocity *= -1
                self.ball.y_velocity = self.calculate_return_y_velocity(self.paddle_left, self.ball)

        if (
            self.ball.y_position >= self.paddle_right.y_position
            and self.ball.y_position <= self.paddle_right.y_position + self.paddle_right.height
        ):
            if self.ball.x_position + self.ball.radius >= self.paddle_right.x_position:
                self.ball.x_velocity *= -1
                self.ball.y_velocity = self.calculate_return_y_velocity(
                    self.paddle_right, self.ball
                )

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
        window.blit(score_two_text, (WINDOW_WIDTH * (3 / 4) - score_two_text.get_width() // 2, 20))

        # Draw the ball
        pygame.draw.circle(
            window,
            self.ball.colour,
            (self.ball.x_position, self.ball.y_position),
            self.ball.radius,
        )

        # Detect if there is a winner
        if self.player_one.score >= MAX_SCORE or self.player_two.score >= MAX_SCORE:
            self.winner(window)
        else:
            pygame.display.update()

    def winner(self, window):
        """Handles writing to the window and resetting the game if a winner is identified.

        Args:
            window (pygame.display): The Pong game window.
        """

        if self.player_one.score >= MAX_SCORE:
            winning_text = f"{self.player_one.name} has won!"
        elif self.player_two.score >= MAX_SCORE:
            winning_text = f"{self.player_two.name} has won!"

        text_to_write = self.game_font.render(winning_text, 1, WHITE)
        window.fill(BLACK)
        window.blit(
            text_to_write,
            (
                WINDOW_WIDTH // 2 - text_to_write.get_width() // 2,
                WINDOW_HEIGHT // 2 - text_to_write.get_height() // 2,
            ),
        )
        self.player_one.score = 0
        self.player_two.score = 0
        pygame.display.update()
        pygame.time.delay(5000)

    def reset(self):
        """Resets the paddle and ball positions as well as ball y_velocity. Ball x_velocity is not impacted."""
        self.ball.x_position = self.ball.x_position_original
        self.ball.y_position = self.ball.y_position_original
        self.ball.y_velocity = 0

        self.paddle_left.y_position = self.paddle_left.y_position_original

        self.paddle_right.y_position = self.paddle_right.y_position_original

    def goal(self):
        """Handles a goal outcome"""
        if self.ball.x_position < 0:
            self.player_two.score += 1
            self.reset()

        elif self.ball.x_position > WINDOW_WIDTH:
            self.player_one.score += 1
            self.reset()

    def run_game(self):
        """Contains the game loop. Handles window closure."""
        run = True
        while run:
            self.clock.tick(FPS_LIMIT)
            self.draw(GAME_WINDOW)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            self.move_paddle(keys)
            self.move_ball()
            self.handle_paddle_collision()
            self.goal()

        pygame.quit()


def main():
    """The entry point to the program"""
    game = Pong()
    game.run_game()


if __name__ == "__main__":
    main()
