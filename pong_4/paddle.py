# TODO - add __str__ support
class Paddle:
    """Paddle class used to create paddles for the pong game."""

    def __init__(self, x_position, y_position, width, height, colour, paddle_velocity=4) -> None:
        """Paddle class init.

        Args:
            x_position (int): current x position
            y_position (int): current y position
            width (int): width in pixels
            height (int): height in pixels
            colour (tuple): paddle fill colour
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
