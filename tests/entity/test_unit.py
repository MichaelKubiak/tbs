from pytest import mark as m

from tests.entity.unit_fixtures import test_unit
from tests.board.board_fixtures import test_board, test_position


@m.describe("Unit")
class TestUnit(object):
    @m.context("When it has multiple orders")
    @m.it("Can determine position at the beginning of a turn")
    def test_pos(self, test_unit):
        assert test_unit.pos(1) == [(0, 0)]
        assert test_unit.pos(2) == [(1, 1)]
        assert test_unit.pos(3) == [(0, 1)]
