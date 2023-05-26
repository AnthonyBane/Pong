import unittest
from pong import Pong, Paddle, Ball

WHITE = (255, 255, 255)


class PongTest(unittest.TestCase):
    def test_init(self):
        paddle = Paddle(x_position=10, y_position=175, width=10, height=100, colour=WHITE)


if __name__ == "__main__":
    unittest.main()
