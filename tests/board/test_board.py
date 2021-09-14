from pytest import mark as m
import pytest

from tbs.board.board import Board, Position
from .board_fixtures import test_board


@m.describe("Position")
class TestPosition(object):
    @m.it("Can equate to an identical Position object")
    def test_equals(self, test_board):
        assert Position(test_board, 0, 0, 0) == Position(test_board, 0, 0, 0)
