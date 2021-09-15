import pytest

from tbs.board.board import Board, Position


@pytest.fixture(scope="function")
def test_board():
    return Board(1, 1)


@pytest.fixture(scope="function")
def test_position(test_board):
    return Position(test_board, 0, 0, 0)
