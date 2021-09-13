import pytest

from tbs.board.board import Board


@pytest.fixture(scope="function")
def test_board():
    return Board(1, 1)
