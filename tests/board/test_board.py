from pytest import mark as m

from tbs.board.board import Board, Position
from .board_fixtures import test_position, test_board


@m.describe("Position")
class TestPosition(object):
    @m.it("Can determine equality")
    def test_equals(self, test_position, test_board):
        assert test_position == Position(test_board, 0, 0, 1)
        assert test_position != Position(test_board, 1, 0, 0)
        assert test_position != Position(test_board, 0, 1, 0)
        assert test_position != Position(test_board, 0, 0, 0)
        assert test_position != (test_board, 0, 0, 1)
