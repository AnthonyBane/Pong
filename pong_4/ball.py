# TODO - add __str__ support
class Ball:
    """Ball class used to create a ball for the ball game."""

    def __init__(
        self,
        x_position: int,
        y_position: int,
        radius: int,
        colour: tuple,
        x_velocity: int = 5,
        y_velocity: int = 0,
        max_velocity: int = 5,
    ) -> None:
        """Ball class init.

        Args:
            x_position (int): current x position.
            y_position (int): current y position.
            radius (int): ball radius in pixels.
            colour (tuple): ball colour fill.
            x_velocity (int, optional): x velocity. Defaults to 5.
            y_velocity (int, optional): y velocity. Defaults to 0.
            max_velocity (int, optional): max potential velocity. Defaults to 5.
        """
        self.x_position = self.x_position_original = x_position
        self.y_position = self.y_position_original = y_position
        self.radius = radius
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.max_velocity = max_velocity
        self.colour = colour

        def __str__(self):
            return f"The ball has an x position of {self.x_position}, y position of {self.y_position}."
