from dataclasses import dataclass


@dataclass
class Player:
    """Example Player class"""

    name: str
    score: int = 0

    def __str__(self) -> str:
        return f'Player "{self.name}" has a score of {self.score}'
