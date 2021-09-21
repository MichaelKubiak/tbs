import pytest

from tbs.entity.entity import Entity, Team
from tbs.board.board import Position, Board

from tests.board.board_fixtures import test_position


class TestEntity(Entity):
    def __init__(self, team: Team, pos: Position):
        self._max_health = 100
        super().__init__(team, pos)
        self._destroyed = False

    @property
    def destroyed(self):
        return self._destroyed

    def pos(self, turn: int):
        pass

    def destroy(self):
        self._destroyed = True


class TestOrder(Entity.Order):
    def __init__(self, entity: Entity, target, length):
        super().__init__(entity, target, length)

    def execute(self):
        pass


@pytest.fixture(scope="function")
def test_entity(test_position):
    """
    A pytest fixture for testing the Entity abstract base class
    """
    return TestEntity(Team.RED, test_position)


@pytest.fixture(scope="function")
def test_order(test_entity, test_position):
    """
    A pytest fixture for testing the Order abstract base class
    """
    return TestOrder(test_entity, test_position, 1)


@pytest.fixture(scope="function")
def test_entity_with_order(test_position, test_order):
    """
    A pytest fixture for testing the Entity abstract base class with multiple
    orders given
    """
    entity = TestEntity(Team.RED, test_position)
    entity.give_order(test_order)
    return entity


@pytest.fixture(scope="function")
def not_test_entity():
    """
    A pytest fixture that is not equal to test_entity for testing __eq__ of the
    Entity abstract base class
    """
    return TestEntity(Team.RED, Position(Board(1, 1), 1, 0, 0))
