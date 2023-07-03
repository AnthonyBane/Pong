"""This module contains two classes, ColourFormat and Colour. 

ColourFormat: This classes handles returning a given RGB colour in different formats.
Colour: This class handles returning a given colour in a specified format, assisted by ColourFormat.

"""

from enum import Enum, auto


class ColourFormat(Enum):
    """Class to handle returning colours in different formats.

    Formats handled are:
        Tuple
        Hex

    Args:
        Enum (enum): Enum super class

    """

    TUPLE = auto()
    HEX = auto()

    @classmethod
    def to_tuple(cls, red: int, green: int, blue: int) -> tuple:
        """Returns a tuple containing red, green, and blue values.

        Args:
            red (int): The red value of RGB colour.
            green (int): The green value of RGB colour.
            blue (int): The blue value of RGB colour.

        Returns:
            tuple: A tuple representation of RGB arguments.
        """
        return (red, green, blue)

    @classmethod
    def to_hex(cls, red: int, green: int, blue: int) -> str:
        """Returns a hex representation of RGB colour.

        Args:
            red (int): The red value of RGB colour.
            green (int): The green value of RGB colour.
            blue (int): The blue value of RGB colour.

        Returns:
            str: Hex string representation of RGB arguments.
        """
        return "#{:02x}{:02x}{:02x}".format(red, green, blue)

    @classmethod
    def colour_formats(cls) -> list:
        """Class method to return a list of colour format options.

        Returns:
            list: A list of colour format options.
        """
        return [member.name for member in ColourFormat]


class Colour(Enum):
    """Colour class to handle colour representations in different formats.

    Format options:
        [0] - RGB
        [1] - Hex

    Args:
        Enum (enum): Enum super class
    """

    WHITE = {"red": 255, "green": 255, "blue": 255}
    BLACK = {"red": 0, "green": 0, "blue": 0}

    def RGB(self, format: ColourFormat = ColourFormat.TUPLE) -> object:
        """Returns an RGB representation of the given colour in a given format.

        Args:
            format (ColourFormat, optional): The format of the returned RGB representation. Defaults to ColourFormat.TUPLE.

        Returns:
            object: A structured RGB representation in the given format.
        """
        match format:
            case ColourFormat.TUPLE:
                return ColourFormat.to_tuple(self.value["red"], self.value["green"], self.value["blue"])
            case ColourFormat.HEX:
                return ColourFormat.to_hex(self.value["red"], self.value["green"], self.value["blue"])

        return None

    @classmethod
    def colour_options(cls) -> list:
        """Returns a list of all colour options

        Returns:
            list: List containing colour options
        """
        return [member.name for member in Colour]
