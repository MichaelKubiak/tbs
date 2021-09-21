import pytest

from tbs.board.board import Board, Position


@pytest.fixture(scope="function")
def test_board():
    """
    A pytest fixture for testing the Board class
    """
    return Board(1, 1)


@pytest.fixture(scope="function")
def test_position(test_board):
    """
    A pytest fixture for testing the Position class
    """
    return Position(test_board, 0, 0, 1)
