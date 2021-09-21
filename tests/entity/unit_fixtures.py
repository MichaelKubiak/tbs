import pytest

from tbs.entity.unit import Unit
from tbs.entity.entity import Team
from tbs.board.board import Position
from tests.entity.entity_fixtures import test_position, TestOrder


class TestUnit(Unit):
    def __init__(self, position):
        self._max_health = 100
        super().__init__(Team.RED, position)


@pytest.fixture(scope="function")
def test_unit(test_position):
    """
    A pytest fixture for testing the unit abstract base class
    """
    test_unit = TestUnit(test_position)
    test_unit.move(Position(test_position.board, 1, 1))
    test_unit.move(Position(test_position.board, 0, 1))
    test_unit.give_order(TestOrder(test_unit, Position(test_position.board, 1, 0), -2))
    return test_unit


# TODO: NEED TO FIND OUT WHAT IS OBSTRUCTING AND WHETHER IT IS ME!!!
