import pong
import pytest


@pytest.fixture
def setup():
    print("------------Test Setup------------")
    game = pong.Pong()
    left_paddle, right_paddle = game.get_paddles()
    ball = game.get_ball()
    yield (game, left_paddle, right_paddle, ball)


def test_y_velocity_calculation(setup):
    game, left_paddle, right_paddle, ball = setup
    y_velocity = game.calculate_return_y_velocity(left_paddle, ball)
    assert y_velocity == 0
    left_paddle.y_position += 10
    y_velocity = game.calculate_return_y_velocity(left_paddle, ball)
    assert y_velocity != 0
