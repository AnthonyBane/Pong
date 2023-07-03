from enum import Enum


class Colour(Enum):
    """Colour class to handle colour representations in different formats.

    Format options:
        [0] - RGB
        [1] - Hex

    Args:
        Enum (enum): Enum super class
    """

    WHITE = ((255, 255, 255), "#FFFFFF")
    BLACK = ((0, 0, 0), "#000000")

    def RGB(self) -> tuple:
        """Returns the RGB value of the called name.

        Returns:
            tuple: A tuple containing the RGB value.
        """
        return self.value[0]

    def hex(self) -> str:
        return self.value[1]
